from pydantic import BaseModel, EmailStr, NonNegativeInt, PositiveInt
from datetime import datetime

from app.schemas.wallet_schema import WalletOut

class EnergyDataOut(BaseModel):
    energy: NonNegativeInt
    last_energy_at: datetime
    completed_at: datetime | None
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