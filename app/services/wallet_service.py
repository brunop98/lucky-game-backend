from typing import Literal

from fastapi import HTTPException
from requests import get
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.wallet import Wallet
from app.services.boost_service import get_active_boost
from app.services.village_service import get_next_cheaper_building_stage_cost


def _get_coins_from_reward_slug(
    db: Session, user: User, reward_slug: Literal["coins_low", "coins_high", "coins_jackpot"]
) -> int:
    cheapest_building_stage_cost = get_next_cheaper_building_stage_cost(db, user)

    if "low" in reward_slug:
        return cheapest_building_stage_cost * 0.04
    elif "high" in reward_slug:
        return cheapest_building_stage_cost * 0.12
    elif "jackpot" in reward_slug:
        return cheapest_building_stage_cost * 0.4


def add_currency(
    db: Session,
    user: User,
    currency: Literal["xp", "coins", "gems", "energy"] | None = None,
    amount: int = None,
    reward_slug: str = None,
):

    # validations
    if not amount and not reward_slug:
        raise Exception("Amount or reward_slug must be provided")
    if amount and reward_slug:
        raise Exception("Amount and reward_slug cannot be provided together")

    if amount and not currency:
        raise Exception("Currency must be provided if amount is provided")
    # ---
    multiplier = 1

    active_boost = get_active_boost(db, user, boost_type=currency)
    if active_boost:
        multiplier = active_boost.multiplier

    allowed_currencies = {"coins", "xp", "gems", "energy"}

    if reward_slug:
        prefix = reward_slug.split("_", 1)[0]

        if prefix not in allowed_currencies:
            raise ValueError(f"Invalid reward_slug: {reward_slug}")

        currency = prefix

        amount = _get_coins_from_reward_slug(db=db, user=user, reward_slug=reward_slug)

    amount = amount * multiplier
    amount = int(amount)
    setattr(user.wallet, currency, getattr(user.wallet, currency) + (amount))
    

    return {
        "reward_data": {"amount": amount, "currency": currency, "multiplier": multiplier},
        "received_at": user.wallet.updated_at,
        "consumable": True,
        "type": "currency",
    }


def deduce_currency(
    db: Session, user: User, currency: Literal["xp", "coins", "gems", "energy"], amount: int
):
    amount = int(amount)
    setattr(user.wallet, currency, getattr(user.wallet, currency) - (amount))


def get_wallet_by_user(db: Session, user: User) -> Wallet:
    print("user ", user)
    return
    # return db.query(Wallet).filter(Wallet.user_id == user_id).first()
