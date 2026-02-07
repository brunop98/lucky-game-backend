from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.helpers.time_helper import utcnow
from app.models.base import Base


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # reward | purchase | spend
    amount = Column(Integer)
    balance_after = Column(Integer)

    # timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow)
