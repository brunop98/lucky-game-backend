from typing import Literal, Union

from pydantic import UUID4, BaseModel, NonNegativeFloat, NonNegativeInt


class CardCoinReward(BaseModel):
    ammount: NonNegativeInt


class CardBoostReward(BaseModel):
    multiplier: NonNegativeFloat
    duration_seconds: NonNegativeInt
    image_url: str


class CardItemReward(BaseModel):
    item_id: NonNegativeInt
    rarity: NonNegativeFloat
    image_url: str
    


class CardReward(BaseModel):
    type: Literal["coins", "boost", "item"]
    reward: Union[CardCoinReward, CardBoostReward, CardItemReward]
    image_url: str


class CardOut(BaseModel):
    id_slug: Literal[
        "coins_low",
        "coins_high",
        "coins_jackpot",
        "boost_low",
        "boost_high",
        "boost_jackpot",
        "rare_item",
    ]
    draw_weight_percent: NonNegativeFloat
    reward: CardReward


class CardRevealIn(BaseModel):
    game_uuid: UUID4 | None = None
