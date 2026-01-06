from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import user_building
from app.models.user import User
from app.models.villages import Villages
from app.models.buildings import Buildings
from app.models.user_building import UserBuilding


def get_building_stage_cost(db: Session, village_id: int, building: Buildings, stage: int) -> int:
    village = db.query(Villages).filter(Villages.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")

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


def get_actual_village_user_building(db: Session, user: User) -> dict:
    actual_village = user.village_level

    rows = (
        db.query(
            Buildings.id,
            Buildings.name,
            Buildings.building_stages,
            Buildings.cost_curve,
            Buildings.base_cost,
            Buildings.cost_multiplier,
            Buildings.created_at,
            Buildings.updated_at,
            UserBuilding.id.label("user_building_id"),
            UserBuilding.current_stage.label("user_building_current_stage"),
            UserBuilding.created_at.label("user_building_created_at"),
            UserBuilding.updated_at.label("user_building_updated_at"),
        )
        .join(Buildings)
        .filter(Buildings.village_id == actual_village, UserBuilding.user_id == user.id)
        .all()
    )

    buildings = []
    for row in rows:
        (
            building_id,
            name,
            building_stages,
            cost_curve,
            base_base_cost,
            cost_multiplier,
            created_at,
            updated_at,
            user_building_id,
            user_building_current_stage,
            user_building_created_at,
            user_building_updated_at,
        ) = row
        building_dict = {
            
            "id": building_id,
            "name": name,
            "building_stages": building_stages,
            "created_at": created_at,
            "updated_at": updated_at,
            "next_stage": {
                "max": user_building_current_stage >= building_stages,
                "cost": (
                    get_building_stage_cost(
                        db, actual_village, row, user_building_current_stage + 1
                    )
                    if user_building_current_stage < building_stages
                    else None
                ),
                # "stage": user_building_current_stage + 1 if user_building_current_stage < building_stages else None,
            },
            "user_building": {"id": user_building_id, "current_stage": user_building_current_stage, "created_at": user_building_created_at, "updated_at": user_building_updated_at},
        }
        buildings.append(building_dict)

    return {"village_level": actual_village, "buildings": buildings}


def next_village(db: Session, village_id: int, user_id: int):
    buildings = db.query(Buildings).filter(Buildings.village_id == village_id).all()

    for building in buildings:
        db.add(UserBuilding(user_id=user_id, building_id=building.id))

    db.flush()
