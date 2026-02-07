from typing import Literal
from fastapi import HTTPException
from pydantic import NonNegativeInt
from sqlalchemy.orm import Session, joinedload

from app.models.building import Building
from app.models.user import User
from app.models.user_building import UserBuilding
from app.models.villages import Villages
from app.schemas.village_schema import BuildingOut, UpdateBuildingOut, VillageOut
from app.services.items_service import add_item
from app.services.xp_service import calculate_building_stage_xp


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


def get_next_stage_info(
    db: Session,
    village: Villages,
    building: Building,
    current_stage: int,
):
    is_max = current_stage >= building.building_stages

    if is_max:
        return {"max": True, "cost": None}

    cost = get_building_stage_cost(db, village, building, current_stage + 1)

    return {"max": False, "cost": cost}


def get_actual_village(db: Session, user: User) -> VillageOut:
    village = db.query(Villages).filter(Villages.id == user.actual_village).first()

    if not village:
        raise HTTPException(status_code=404, detail="Village not found")

    user_buildings = (
        db.query(UserBuilding)
        .options(joinedload(UserBuilding.building))
        .filter(UserBuilding.user_id == user.id)
        .all()
    )

    buildings_out = []

    for ub in user_buildings:
        building = ub.building

        next_stage = get_next_stage_info(db, village, building, ub.current_stage)

        buildings_out.append(
            BuildingOut.model_validate(
                {
                    **building.__dict__,
                    "next_stage": next_stage,
                    "user_building": ub,
                }
            )
        )

    buildings_out.sort(key=lambda b: b.id)

    return VillageOut(
        id=village.id,
        name=village.name,
        completion_reward={
            "coins": village.starting_reward_coins,
            "gems": village.starting_reward_gems,
            "energy": village.starting_reward_energy,
            "item_slug": village.starting_reward_item_slug,
        },
        buildings=buildings_out,
    )


def _get_next_village(db: Session, current_village: Villages | None = None) -> Villages | None:
    if current_village is None:
        return db.query(Villages).filter(Villages.id == 1).first()

    return db.query(Villages).filter(Villages.id == current_village.id + 1).first()


def next_village(
    db: Session,
    user: User,
    current_village: Villages | None = None,
):
    from app.services.wallet_service import add_currency

    
    

    next_village = _get_next_village(db, current_village)

    if next_village is None:
        # TODO: all villages upgraded → reset
        # reset:
        # - increment formulas in add_currency
        # - reset user_buildings, energy, coins
        # - keep xp and gems
        pass

    add_currency(db, user, "coins", next_village.starting_reward_coins)
    add_currency(db, user, "gems", next_village.starting_reward_gems)
    add_currency(db, user, "energy", next_village.starting_reward_energy)
    add_currency(db, user, "xp", next_village.starting_reward_xp)

    try:
        add_item(db, user, next_village.starting_reward_item_slug)
    except Exception:
        pass

    buildings = db.query(Building).filter(Building.village_id == next_village.id).all()

    for building in buildings:
        db.add(UserBuilding(user_id=user.id, building_id=building.id))

    next_village = _get_next_village(db, current_village)

    user.actual_village = next_village.id

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


def _check_village_completion(db: Session, user: User):
    user_buildings = (
        db.query(UserBuilding)
        .options(joinedload(UserBuilding.building))
        .filter(UserBuilding.user_id == user.id)
        .all()
    )

    if all(ub.current_stage >= ub.building.building_stages for ub in user_buildings):
        return True

    return False


def upgrade_building(db: Session, user: User, building_id: int) -> UpdateBuildingOut:
    from app.services.wallet_service import _deduce_currency, add_currency

    ub = (
        db.query(UserBuilding)
        .filter(UserBuilding.user_id == user.id, UserBuilding.building_id == building_id)
        .first()
    )

    if not ub:
        raise HTTPException(status_code=404, detail="User building not found")

    building = db.query(Building).filter(Building.id == building_id).first()
    village = db.query(Villages).filter(Villages.id == ub.building.village_id).first()

    stage_cost = get_building_stage_cost(db, village, building, ub.current_stage + 1)

    if user.wallet.coins < stage_cost:
        raise HTTPException(status_code=400, detail="Not enough coins to upgrade building")

    if ub.current_stage < building.building_stages:
        ub.current_stage += 1

    _deduce_currency(db, user, "coins", stage_cost)

    xp_to_add = calculate_building_stage_xp(building.base_completion_reward_xp, ub.current_stage)
    add_currency(db, user, "xp", xp_to_add)
    upgraded_village = False
    if _check_village_completion(db, user):
        next_village(db, user, village)
        upgraded_village = True

    return {
        "message": "Building upgraded successfully",
        "cost": stage_cost,
        "upgraded_village": upgraded_village,
        "xp_earned": xp_to_add,
        "building_current_stage": ub.current_stage,
    }
