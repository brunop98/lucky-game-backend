from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Float,
    Integer,
    ForeignKey,
    DateTime,
    String,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
import uuid


class CardHash(Base):
    __tablename__ = "card_hashes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    
   
    reward_probability = Column(Float, nullable=False)
    reward_focus = Column(String, nullable=False, index=True)

    item_slug = Column(String, ForeignKey("items.slug"), nullable=True)

    # estado
    used = Column(Boolean, nullable=False, default=False)
    canceled = Column(Boolean, nullable=False, default=False)

    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relations
    user = relationship("User", back_populates="card_hash")
    item = relationship("Item", back_populates="card_hash")


    __table_args__ = (
        CheckConstraint(
            "reward_focus IN ('rare_item', 'coins_jackpot')", name="ck_card_hashes_reward_focus"
        ),
    )
