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
    # TODO: quando a tabela de itens for criada, definir esse schema


class CardReward(BaseModel):
    type: Literal["coin", "buff", "item"]
    reward: Union[CardCoinReward, CardBoostReward, CardItemReward]
    image_url: str


class CardOut(BaseModel):
    id_slug: Literal[
        "coin_low",
        "coin_medium",
        "coin_jackpot",
        "boost_low",
        "boost_medium",
        "boost_jackpot",
        "rare_item",
        "common_item",
    ]
    draw_weight_percent: NonNegativeFloat  
    reward: CardReward

class CardRevealIn(BaseModel):
    game_hash: UUID4 | None = None
