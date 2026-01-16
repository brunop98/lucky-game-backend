import random
import re
from typing import Literal
from uuid import uuid4, UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.building import Building
from app.models.item import Item
from app.models.user import User
from app.models.user_building import UserBuilding
from app.models.card_hash import CardHash
from app.services.items_service import user_has_item

ALLOWED_REWARD_FOCUS = {
    "rare_item",
    "coin_jackpot", 
}

BASE_PROBABILITIES = {
    "rare_item": 0.03,      # 3.0%
    "coin_jackpot": 0.01,   # 1.0%
}

MIN_PROBABILITIES = {
    "rare_item": 0.015,    # 1.5%
    "coin_jackpot": 0.005, # 0.5%
}


def sort_card(db: Session, user: User, game_data, card_hash):
    return


def get_coins_reward(
    db: Session, user: User, reward_focus: Literal["coin_low", "coin_medium", "jackpot"]
):
    user_buildings = (
        db.query(UserBuilding).filter(UserBuilding.user_id == user.id).join(Building).all()
    )
    return user_buildings


def get_game_data(db: Session, user: User, game_uuid: UUID):
    card_data = (
        db.query(CardHash).filter(CardHash.user_id == user.id, CardHash.id == game_uuid).first()
    )

    if card_data is None:
        raise HTTPException(status_code=404, detail="Card not found")

    if card_data.used:
        raise HTTPException(status_code=400, detail="Card already used")

    if card_data.canceled:
        raise HTTPException(status_code=400, detail="Card canceled")

    return {
        "reward_focus": "rare_item" if card_data.item_slug else "coin_jackpot",
        "item_slug": card_data.item_slug,
    }


# PROBABILITY



# HASH


def cancel_game_uuid(db: Session, user: User, game_uuid: UUID):
    db.query(CardHash).filter(CardHash.user_id == user.id, CardHash.id == game_uuid).update(
        {"canceled": True}
    )
    db.commit()
    return


def _create_game(
    db: Session,
    user: User,
    reward_focus: str,
    item_slug: str | None,
) -> CardHash:

    probability = get_reward_probability(
        user=user,
        reward_focus=reward_focus,
    )

    card = CardHash(
        id=uuid4(),
        user_id=user.id,
        reward_focus=reward_focus,
        reward_probability=probability,
        item_slug=item_slug,
    )

    db.add(card)
    db.commit()
    db.refresh(card)

    return card


def _search_active_card_hash(
    db: Session,
    user_id: int,
    reward_focus: str,
    item_slug: str | None,
) -> CardHash | None:
    return (
        db.query(CardHash)
        .filter(
            CardHash.user_id == user_id,
            CardHash.reward_focus == reward_focus,
            CardHash.item_slug == item_slug,
            CardHash.used.is_(False),
            CardHash.canceled.is_(False),
        )
        .first()
    )


def create_or_get_game(
    db: Session,
    user: User,
    goal_card: str | None,
) -> CardHash:
    """
    Regra:
    - goal_card != None → jogo de ITEM
    - goal_card == None → jogo de JACKPOT
    """

    if goal_card:
        reward_focus = "rare_item"

        item = db.query(Item).filter(Item.slug == goal_card).first()
        if not item:
            raise HTTPException(400, "Item not found")

        if not item.drawn_available:
            raise HTTPException(400, "Item not available")
        
        if user_has_item(db, user, item):
            raise HTTPException(400, "User already has item")
        

        item_slug = item.slug

    else:
        reward_focus = "coin_jackpot"
        item_slug = None

    existing = _search_active_card_hash(
        db=db,
        user_id=user.id,
        reward_focus=reward_focus,
        item_slug=item_slug,
    )

    if existing:
        return existing

    return _create_game(
        db=db,
        user=user,
        reward_focus=reward_focus,
        item_slug=item_slug,
    )


# reward sort
from datetime import datetime, timezone

def get_reward_probability(
    user: User,
    reward_focus: str,
) -> float:
    """
    Retorna probabilidade FINAL em %
    Ex: 0.01 = 1%
    """

    if reward_focus not in ALLOWED_REWARD_FOCUS:
        raise HTTPException(400, "Invalid reward focus")

    base = BASE_PROBABILITIES[reward_focus]
    probability = base

    # --------------------
    # PITY SYSTEM (apenas rare_item)
    # --------------------
    if reward_focus == "rare_item":
        pity_count = user.rare_item_miss_count
        pity_bonus = min(pity_count * 0.0015, 0.03)  # +0.15% por falha (cap 3%)
        probability += pity_bonus
        print('pity_bonus', pity_bonus)

    # --------------------
    # JACKPOT COOLDOWN (sem bloqueio)
    # --------------------
    if reward_focus == "coin_jackpot" and user.last_jackpot_at:
        now = datetime.now(timezone.utc)
        minutes = (now - user.last_jackpot_at).total_seconds() / 60

        if minutes < 30:
            # penalidade máxima = base - mínimo
            max_penalty = base - MIN_PROBABILITIES["coin_jackpot"]

            # decaimento linear
            cooldown_penalty = max_penalty * ((30 - minutes) / 30)
            probability -= cooldown_penalty

    # --------------------
    # Garantia de mínimo
    # --------------------
    probability = max(probability, MIN_PROBABILITIES[reward_focus])

    # arredondamento seguro (ex: 0.0075 → 0.75%)
    return round(probability, 4)
