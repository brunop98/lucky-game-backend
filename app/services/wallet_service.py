import re
from typing import Literal
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.wallet import Wallet
from app.services.village_service import get_next_cheaper_building_stage_cost


def _get_coins_from_reward_slug(db: Session, user: User, reward_slug: str) -> int:
    cheapest_building_stage_cost = get_next_cheaper_building_stage_cost(db, user)

    if "low" in reward_slug:
        return cheapest_building_stage_cost * 0.04
    elif "medium" in reward_slug:
        return cheapest_building_stage_cost * 0.12
    elif "jackpot" in reward_slug:
        return cheapest_building_stage_cost * 0.4
    
    raise Exception(f"Invalid reward_slug: {reward_slug}")


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
    if reward_slug:
        if "coins" in reward_slug:
            currency = "coins"
            amount = _get_coins_from_reward_slug(db=db, user=user, reward_slug=reward_slug)

    
    setattr(user.wallet, currency, getattr(user.wallet, 'coins') + amount)
    db.commit()
    db.refresh(user.wallet)

    return


def get_wallet_by_user(db: Session, user: User) -> Wallet:
    print("user ", user)
    return
    # return db.query(Wallet).filter(Wallet.user_id == user_id).first()
