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
) -> VillageOut:

    return get_actual_village(db, current_user)

@router.post("/update-building")
def update_building(
    payload: UpdateBuildingIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return upgrade_building(db, current_user, payload.building_id)
