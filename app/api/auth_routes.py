from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.auth_facebook import (
    validate_facebook_token,
    get_facebook_user,
)
from app.services.auth_service import get_or_create_user_with_wallet

router = APIRouter(prefix="/login", tags=["auth"])


# ⚠️ DEV ONLY – remover em produção
@router.post("/dev")
def dev_login(db: Session = Depends(get_db)):
    user, wallet = get_or_create_user_with_wallet(
        db=db,
        facebook_id="DEV_USER",
        name="Dev User"
    )

    return {
        "id": user.id,
        "facebook_id": user.facebook_id,
        "name": user.name,
        "balance": wallet.balance
    }


@router.post("/facebook")
def facebook_login(payload: dict, db: Session = Depends(get_db)):
    token = payload.get("access_token")
    if not token:
        raise HTTPException(400, "Token ausente")

    if not validate_facebook_token(token):
        raise HTTPException(401, "Token inválido")

    fb = get_facebook_user(token)

    user, wallet = get_or_create_user_with_wallet(
        db=db,
        facebook_id=fb["id"],
        name=fb["name"]
    )

    return {
        "id": user.id,
        "name": user.name,
        "balance": wallet.balance
    }
