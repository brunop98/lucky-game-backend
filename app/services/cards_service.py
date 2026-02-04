import random
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.building import Building
from app.models.card_hash import CardHash
from app.models.item import Item
from app.models.user import User
from app.models.user_building import UserBuilding
from app.services.boost_service import trigger_boost
from app.services.items_service import add_item, user_has_item
from app.services.wallet_service import add_currency, _deduce_currency, get_wallet_by_user

ALLOWED_REWARD_FOCUS = {
    "rare_item",
    "coins_jackpot",
}

BASE_PROBABILITIES = {
    "rare_item": 0.03,  # 3.0%
    "coins_jackpot": 0.01,  # 1.0%
}

MIN_PROBABILITIES = {
    "rare_item": 0.015,  # 1.5%
    "coins_jackpot": 0.005,  # 0.5%
}

ALTERNATIVE_REWARDS_PROBABILITIES = {
  "coins_low": 0.37,
  "coins_high": 0.24,
  "boost_low": 0.12,
  "boost_high": 0.09,
  "boost_jackpot": 0.04,
  "energy_low": 0.10,
  "energy_high": 0.04 
}



def sort_card(db: Session, user: User, game_data, card_hash):
    return


def get_coins_reward(
    db: Session, user: User, reward_focus: Literal["coins_low", "coins_high", "jackpot"]
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
        "reward_focus": "rare_item" if card_data.item_slug else "coins_jackpot",
        "item_slug": card_data.item_slug,
    }


# HASH


def cancel_game_uuid(db: Session, user: User, game_uuid: UUID):
    db.query(CardHash).filter(CardHash.user_id == user.id, CardHash.id == game_uuid).update(
        {"canceled": True}
    )
    return


def _create_game(
    db: Session,
    user: User,
    reward_focus: str,
    item_slug: str | None,
) -> CardHash:

    probability = _get_reward_probability(
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


def _get_reward_probability(
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
        print("pity_bonus", pity_bonus)

    # --------------------
    # JACKPOT COOLDOWN (sem bloqueio)
    # --------------------
    if reward_focus == "coins_jackpot" and user.last_jackpot_at:
        now = datetime.now(timezone.utc)
        minutes = (now - user.last_jackpot_at).total_seconds() / 60

        if minutes < 30:
            # penalidade máxima = base - mínimo
            max_penalty = base - MIN_PROBABILITIES["coins_jackpot"]

            # decaimento linear
            cooldown_penalty = max_penalty * ((30 - minutes) / 30)
            probability -= cooldown_penalty

    # --------------------
    # Garantia de mínimo
    # --------------------
    probability = max(probability, MIN_PROBABILITIES[reward_focus])

    # arredondamento seguro (ex: 0.0075 → 0.75%)
    return round(probability, 4)


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

    if user.wallet.energy < 1: 
        raise HTTPException(400, "Not enough energy") 

    if goal_card:
        reward_focus = "rare_item"

        item = db.query(Item).filter(Item.slug == goal_card).first()
        if user_has_item(db, user, item):
            raise HTTPException(400, "User already has item")

        if not item.drawn_available:
            raise HTTPException(400, "Item not available")

        item_slug = item.slug

    else:
        reward_focus = "coins_jackpot"
        item_slug = None

    existing = _search_active_card_hash(
        db=db,
        user_id=user.id,
        reward_focus=reward_focus,
        item_slug=item_slug,
    )

    _deduce_currency(db, user, "energy", 1)

    if existing:
        return existing

    return _create_game(
        db=db,
        user=user,
        reward_focus=reward_focus,
        item_slug=item_slug,
    )


def _draw_weighted():
    total = sum(ALTERNATIVE_REWARDS_PROBABILITIES.values())

    if not abs(total - 1.0) < 1e-6:
        raise ValueError(f"Probabilities must sum to 1.0, got {total}")

    rewards = list(ALTERNATIVE_REWARDS_PROBABILITIES.keys())
    weights = list(ALTERNATIVE_REWARDS_PROBABILITIES.values())

    return random.choices(rewards, weights=weights, k=1)[0]


def draw_card_weighted(
    db: Session,
    user: User,
    game_uuid: UUID,
):
    card_hash = db.query(CardHash).filter(CardHash.id == game_uuid).first()

    if not card_hash:
        raise HTTPException(404, "Card not found")

    if card_hash.used:
        raise HTTPException(400, "Card already used")

    if card_hash.canceled:
        raise HTTPException(400, "Card canceled")

    focus_reward_probability = card_hash.reward_probability
    focus_reward = card_hash.reward_focus

    result = None

    won_focus_reward = random.random() < focus_reward_probability
    if won_focus_reward:
        if focus_reward == "rare_item":
            if user_has_item(db, user, card_hash.item_slug):
                card_hash.canceled = True

                raise HTTPException(400, "User already has item")

            result = add_item(db, user, card_hash.item_slug)
        else:
            result = add_currency(db, user, currency="coins", reward_slug="coins_jackpot")
    else:
        alternative_reward = _draw_weighted()

        if "coins" in alternative_reward:
            result = add_currency(db, user, currency="coins", reward_slug=alternative_reward)
        elif "boost" in alternative_reward:
            result = trigger_boost(db, user, alternative_reward, boost_type="xp")
        elif "energy" in alternative_reward:
            result = add_currency(db, user, currency="energy", reward_slug=alternative_reward)
    
    # card_hash.used = True

    return result
