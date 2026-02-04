from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.items_service import user_has_item as user_has_item_service

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/user-has-item/{item_slug}")
def user_has_item(
    item_slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        hasItem = user_has_item_service(db, current_user, item_slug)
        db.commit()
        return {
            "hasItem": hasItem,
        }
    except HTTPException as e:
        db.rollback()
        raise
