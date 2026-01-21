from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.auth import get_current_user
from app.models import CardHash
from app.models.item import Item
from app.models.user import User
from app.schemas.card_schema import NewGameIn, NewGameOut, RevealCardIn
from app.schemas.reward_schema import RewardOut
from app.services.cards_service import (
    create_or_get_game,
    draw_card_weighted,
    get_coins_reward,
    get_game_data,
    cancel_game_uuid,
)
from app.services.items_service import add_item, user_has_item
from app.services.wallet_service import add_currency

router = APIRouter(prefix="/cards", tags=["cards"])


@router.delete("/cancel/{game_uuid}")
def cancel_game(
    game_uuid: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    cancel_game_uuid(db, current_user, game_uuid)
    return {"message": "Game canceled", "game_uuid": game_uuid}


@router.get("/new-game")
def new_game(
    query: NewGameIn = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NewGameOut:
    game = create_or_get_game(
        db=db,
        user=current_user,
        goal_card=query.goal_card,
    )

    return {
        "game_uuid": game.id,
        "reward_focus": game.reward_focus,
        "reward_probability": game.reward_probability,
        "item_slug": game.item_slug,
    }


@router.post("/reveal-card") 
def reveal_card(
    payload: RevealCardIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
)-> RewardOut:
    return draw_card_weighted(db, current_user, payload.game_uuid)
    # save current_user on db
