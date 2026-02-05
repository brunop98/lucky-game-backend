from datetime import datetime, timedelta
from typing import Literal

from fastapi import HTTPException
from requests import get
from sqlalchemy.orm import Session

from app.helpers.time import utcnow
from app.models.user import User
from app.models.wallet import Wallet
from app.services.boost_service import get_active_boost_multiplier
from app.services.village_service import get_next_cheaper_building_stage_cost

MAX_ENERGY_COUNT = 10
MAX_ENERGY_SECONDS = 600
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
    
def _get_energy_from_reward_slug(
    db: Session, user: User, reward_slug: Literal["energy_low", "energy_high"]
) -> int:

    if "low" in reward_slug:
        return 1
    elif "high" in reward_slug:
        return 3


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

    active_boost = get_active_boost_multiplier(db, user, boost_type=currency)
    if active_boost:
        multiplier = active_boost.multiplier

    allowed_currencies = {"coins", "xp", "gems", "energy"}

    if reward_slug:
        prefix = reward_slug.split("_", 1)[0]

        if prefix not in allowed_currencies:
            raise ValueError(f"Invalid reward_slug: {reward_slug}")

        currency = prefix

        if prefix == "coins":
            amount = _get_coins_from_reward_slug(db=db, user=user, reward_slug=reward_slug)
        elif prefix == "energy":
            amount = _get_energy_from_reward_slug(db=db, user=user, reward_slug=reward_slug)
    if currency == "coins":
        amount = amount * multiplier
        # TODO reset multiplier
    if currency == "energy":
        amount = min(amount, MAX_ENERGY_COUNT)
    
    amount = int(amount)
    
    setattr(user.wallet, currency, getattr(user.wallet, currency) + (amount))



    return {
        "reward_data": {"amount": amount, "currency": currency, "multiplier": multiplier},
        "received_at": user.wallet.updated_at,
        "consumable": True,
        "type": "currency",
    }


def _deduce_currency(
    db: Session, user: User, currency: Literal["xp", "coins", "gems", "energy"], amount: int
):
    amount = int(amount)
    setattr(user.wallet, currency, getattr(user.wallet, currency) - (amount))


def get_wallet_by_user(db: Session, user: User) -> Wallet:
    print("user ", user)
    return

def _calculate_energy_gain(last_energy_at: datetime) -> int:
    elapsed_seconds = (utcnow() - last_energy_at).total_seconds()
    return max(0, int(elapsed_seconds // MAX_ENERGY_SECONDS))

def _apply_energy_regen(db: Session, user: User) -> None:
    gained = _calculate_energy_gain(user.wallet.last_energy_at)

    if gained <= 0:
        return

    missing = MAX_ENERGY_COUNT - user.wallet.energy
    to_add = min(gained, missing)

    if to_add <= 0:
        return

    add_currency(db, user, "energy", to_add)

    user.wallet.last_energy_at += timedelta(
        seconds=to_add * MAX_ENERGY_SECONDS
    )
def get_energy_data(db: Session, user: User) -> dict:
    _apply_energy_regen(db, user)

    now = utcnow()
    last_energy_at = user.wallet.last_energy_at

    elapsed = (now - last_energy_at).total_seconds()
    seconds_to_next = max(0, MAX_ENERGY_SECONDS - elapsed)

    will_complete_at = (
        last_energy_at + timedelta(seconds=MAX_ENERGY_SECONDS)
        if user.wallet.energy < MAX_ENERGY_COUNT
        else None
    )

    return {
        "current_enernegy_count": user.wallet.energy,
        "next_enernegy_count": (user.wallet.energy + 1) if user.wallet.energy < MAX_ENERGY_COUNT else MAX_ENERGY_COUNT,
        "last_energy_at": last_energy_at,
        "will_complete_at": will_complete_at,
        "max": user.wallet.energy >= MAX_ENERGY_COUNT
    }
