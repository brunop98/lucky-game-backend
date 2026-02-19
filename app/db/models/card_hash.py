import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.helpers.time_helper import utcnow


class CardHash(Base):
    __tablename__ = "card_hashes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    reward_probability = Column(Float, nullable=False)
    reward_focus = Column(String, nullable=False, index=True)

    item_slug = Column(String, ForeignKey("items.slug"), nullable=True)

    # estado
    used = Column(Boolean, nullable=False, default=False)
    canceled = Column(Boolean, nullable=False, default=False)

    # timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow)

    # relations
    user = relationship("User", back_populates="card_hash")
    item = relationship("Item", back_populates="card_hash")

    __table_args__ = (
        CheckConstraint(
            "reward_focus IN ('rare_item', 'coins_jackpot')", name="ck_card_hashes_reward_focus"
        ),
    )
