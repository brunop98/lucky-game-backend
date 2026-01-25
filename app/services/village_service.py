from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.building import Building
from app.models.user import User
from app.models.user_building import UserBuilding
from app.models.villages import Villages
from app.schemas.village_schema import UpdateBuildingOut


def get_building_stage_cost(db: Session, village: Villages, building: Building, stage: int) -> int:

    if not building:
        raise HTTPException(status_code=404, detail="Building not found in the specified village")

    if stage < 1 or stage > building.building_stages:
        raise HTTPException(status_code=400, detail="Invalid building stage")

    if building.cost_curve == "exponential":
        cost = round(
            building.base_cost
            * village.building_cost_modifier
            * (building.cost_multiplier ** (stage - 1))
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported cost curve")

    return cost


def get_actual_village(db: Session, user: User) -> dict:
    village = db.query(Villages).filter(Villages.id == user.actual_village).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")

    user_buildings = (
        db.query(UserBuilding)
        .filter(UserBuilding.user_id == user.id)
        .all()
    )

    buildings = []
    for ub in user_buildings:
        building = db.query(Building).filter(Building.id == ub.building_id).first()
        next_stage_cost = (
            get_building_stage_cost(db, village, building, ub.current_stage + 1)
            if ub.current_stage < building.building_stages
            else None
        )

        buildings.append({
            "id": building.id,
            "name": building.name,
            "building_stages": building.building_stages,
            "created_at": building.created_at,
            "updated_at": building.updated_at,
            "next_stage": {
                "max": ub.current_stage >= building.building_stages,
                "cost": next_stage_cost,
            },
            "user_building": {
                "id": ub.id,
                "current_stage": ub.current_stage,
                "created_at": ub.created_at,
                "updated_at": ub.updated_at,
            }
        })
    buildings = sorted(buildings, key=lambda x: x["id"])
    return {
        "id": village.id,
        "name": village.name,
        "completion_reward": {
            "coins": village.completion_reward_coins,
            "gems": village.completion_reward_gems,
            "energy": village.completion_reward_energy,
            "item_id": village.completion_reward_item_id,
        },
        "buildings": buildings,
    }



def next_village(db: Session, village_id: int, user_id: int):
    buildings = db.query(Building).filter(Building.village_id == village_id).all()

    for building in buildings:
        db.add(UserBuilding(user_id=user_id, building_id=building.id))

    db.flush()


def get_next_cheaper_building_stage_cost(db: Session, user: User) -> int | None:
    candidates = (
        db.query(UserBuilding)
        .join(Building)
        .join(Villages)
        .filter(
            UserBuilding.user_id == user.id,
            Villages.id == user.actual_village,
            UserBuilding.current_stage < Building.building_stages,
        )
        .all()
    )

    if not candidates:
        return None

    cheapest = min(
        candidates,
        key=lambda ub: get_building_stage_cost(
            db,
            ub.building.village,
            ub.building,
            ub.current_stage + 1,
        ),
    )

    cheapest_value = get_building_stage_cost(
        db,
        cheapest.building.village,
        cheapest.building,
        cheapest.current_stage + 1,
    )

    return cheapest_value


def upgrade_building(db: Session, user: User, building_id: int) -> UpdateBuildingOut:
    from app.services.wallet_service import deduce_currency

    # TODO: add xp
    # TODO: if all buildings are upgraded at the village, upgrade the village

    ub = db.query(UserBuilding).filter(
        UserBuilding.user_id == user.id,
        UserBuilding.building_id == building_id
    ).first()

    building = db.query(Building).filter(Building.id == building_id).first()
    village = db.query(Villages).filter(Villages.id == ub.building.village_id).first()

    stage_cost = get_building_stage_cost(db, village, building, ub.current_stage + 1)

    if user.wallet.coins < stage_cost:
        raise HTTPException(status_code=400, detail="Not enough coins to upgrade building")

    if ub.current_stage < building.building_stages:
        ub.current_stage += 1

    deduce_currency(db, user, "coins", stage_cost)
    db.commit()

    return {
        "message": "Building upgraded successfully",
        "cost": stage_cost,
    }


