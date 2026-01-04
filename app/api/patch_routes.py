from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.cards_service import generate_new_game_cards
from app.services.content_patch_service import get_active_patch

router = APIRouter(prefix="/patch", tags=["patch"])

@router.get("/latest")
def get_latest_patch(db: Session = Depends(get_db)):
    """
    Endpoint público.
    Retorna informações do último patch ativo.
    """
    return get_active_patch(db)