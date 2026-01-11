from sqlalchemy import Boolean, Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class CardHash(Base):
    # TODO verificar a necessidade de rare_item_probability e jackpot_probability
    __tablename__ = "card_hashes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"),  nullable=False)
    item_slug = Column(String, ForeignKey("items.slug"), nullable=True)

    used = Column(Boolean, nullable=False, default=False)
    canceled = Column(Boolean, nullable=False, default=False)

    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="card_hash")
    item = relationship(
        "Item",
        back_populates="card_hash"
    )
