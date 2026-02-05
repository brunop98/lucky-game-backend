from pydantic import BaseModel, EmailStr, NonNegativeFloat, NonNegativeInt, PositiveInt
from datetime import datetime

from app.schemas.wallet_schema import WalletOut


# MULTIPLIERS
class BoostDataOut(BaseModel):
    boost_type: str
    multiplier: NonNegativeFloat
    starts_at: datetime
    ends_at: datetime 
    source: str | None

class ResetDataOut(BaseModel):
    multiplier: PositiveInt
    reset_count: NonNegativeInt

class MultipliersOut(BaseModel):
    reset: ResetDataOut
    boosts: list[BoostDataOut]

# ENERGY
class EnergyDataOut(BaseModel):
    current_enernegy_count: NonNegativeInt
    next_enernegy_count: NonNegativeInt
    last_energy_at: datetime
    will_complete_at: datetime | None
    max: bool

# USER
class XpOut(BaseModel):
    user_level: NonNegativeInt
    current_xp: NonNegativeInt
    xp_to_current_level: NonNegativeInt
    xp_to_next_level: NonNegativeInt

class UserOut(BaseModel):
    full_name: str
    email: EmailStr | None 
    locale: str | None 
    rank: PositiveInt
    created_at: datetime
    updated_at: datetime | None     
    wallet: WalletOut
    xp: XpOut

    class Config:
        from_attributes = True