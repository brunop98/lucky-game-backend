from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.village_service import get_actual_village_user_building

router = APIRouter(prefix="/village", tags=["village"])

@router.get("")
def get_village_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    return get_actual_village_user_building(db, current_user)


