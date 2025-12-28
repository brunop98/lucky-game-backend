from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Wallet

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("/{user_id}")
def get_wallet(user_id: int, db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter_by(user_id=user_id).first()

    if not wallet:
        raise HTTPException(404, "Wallet não encontrada")

    return {"balance": wallet.balance}
