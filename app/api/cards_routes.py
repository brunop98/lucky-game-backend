from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.card_schema import CardOut
from app.services.cards_service import (
    get_rare_item_probability,
    get_game_uuid,
    get_jackpot_probability,
    cancel_game_uuid,
)

router = APIRouter(prefix="/cards", tags=["cards"])


@router.delete("/cancel/{game_uuid}")
def cancel_game(
    game_uuid: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    cancel_game_uuid(db, current_user, game_uuid)
    return {"message": "Game canceled", "game_uuid": game_uuid}


@router.get("/new-game")
def new_game(
    goal_card: Optional[str] = Query(
        None
    ),  # goal_card eh o item_slug por enquanto, mas pode ser adicionado mais coisas
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: logica para gerar cartas baseado no usuario, historico, etc.
    # TODO impedir ganhar item repetido
    # TODO TESTAR MUITO

    new_game = {
        "game_uuid": get_game_uuid(db, current_user, goal_card or None),
        "rare_item_probability": (
            0 if not goal_card else get_rare_item_probability(db, current_user, goal_card)
        ),
        "jackpot_probability": (
            0 if goal_card else get_jackpot_probability(db, current_user, goal_card)
        ),
    }

    return new_game


@router.post("/reveal-card")
def reveal_card(
    payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> CardOut:
    card = payload.get("revealed_card")

    if not card:
        raise HTTPException(400, "Card is required")

    # TODO: add to inventory/wallet
    # TODO impedir de ganhar item repetido
    return {"revealed_card": card}
