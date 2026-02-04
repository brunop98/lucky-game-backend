from pydantic import BaseModel, EmailStr, NonNegativeInt, PositiveInt
from datetime import datetime

from app.schemas.wallet_schema import WalletOut

class EnergyDataOut(BaseModel):
    current_enernegy_count: NonNegativeInt
    next_enernegy_count: NonNegativeInt
    last_energy_at: datetime
    will_complete_at: datetime | None
    max: bool

class UserOut(BaseModel):
    full_name: str
    email: EmailStr | None 
    locale: str | None 
    rank: PositiveInt
    created_at: datetime
    updated_at: datetime | None     
    wallet: WalletOut

    class Config:
        from_attributes = True