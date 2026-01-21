from datetime import datetime
from typing import Literal

from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt


class CurrencyReward(BaseModel):
    amount: NonNegativeInt
    currency: Literal["xp", "coins", "gems", "energy"]
    multiplier: NonNegativeFloat


class ItemReward(BaseModel):
    item_slug: str
    stack_size: NonNegativeInt


class BoostReward(BaseModel):
    multiplier: NonNegativeFloat
    duration_seconds: NonNegativeInt


class RewardOut(BaseModel):
    type: Literal["currency", "boost", "item"]
    consumable: bool
    received_at: datetime
    reward_data: CurrencyReward | BoostReward | ItemReward
