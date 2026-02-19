from locale import currency
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.helpers.time_helper import utcnow
from app.models.base import Base


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    type = Column(String)  # earn | spend
    amount = Column(Integer)
    balance_after = Column(Integer)
    currency = Column(String)

    # timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow)

    user = relationship("User", back_populates="wallet_transactions") 

    __table_args__ = (
        # garante unicidade por provider
        {"sqlite_autoincrement": True},
    )
