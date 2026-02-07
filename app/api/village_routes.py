from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.village_schema import UpdateBuildingIn, VillageOut
from app.services.village_service import get_actual_village, upgrade_building

router = APIRouter(prefix="/village", tags=["village"])


@router.get("")
def get_village(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
): #TODO aplicar -> VillageOut:
    try:
        actual_village = get_actual_village(db, current_user)
        db.commit()
        return actual_village
    except HTTPException as e:
        db.rollback()
        raise

@router.post("/update-building")
def update_building(
    payload: UpdateBuildingIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        upgraded_building = upgrade_building(db, current_user, payload.building_id)
        db.commit()
        return upgraded_building
    except HTTPException as e:
        db.rollback()
        raise
