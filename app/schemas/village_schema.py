from datetime import datetime
from typing import Optional
from pydantic import BaseModel, NonNegativeInt, PositiveInt

from app.schemas.building_schema import BuildingOut


class NextStageOut(BaseModel):
    max: bool
    cost: Optional[int]



class UserBuildingOut(BaseModel):
    id: int
    current_stage: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class BuildingOut(BaseModel):
    id: int
    name: str
    building_stages: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    next_stage: NextStageOut
    user_building: UserBuildingOut



class CompletionRewardOut(BaseModel):
    coins: int
    gems: int
    energy: int
    item_slug: Optional[str]


class VillageOut(BaseModel):
    id: int
    name: str
    reset_available: bool
    completion_reward: CompletionRewardOut
    buildings: list[BuildingOut]


class UpdateBuildingIn(BaseModel):
    building_id: NonNegativeInt


class UpdateBuildingOut(BaseModel):
    message: str
    cost: NonNegativeInt
    upgraded_village: bool
