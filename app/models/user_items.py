from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class UserItem(Base):
    __tablename__ = "user_buildings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    stack_size = Column(Integer, nullable=False, default=1)

    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        {"sqlite_autoincrement": True},
        CheckConstraint("stack_size > 0", name="ck_cards_stack_size_positive"),
    )

    user = relationship(
        "User",
        back_populates="user_items"
    )

    item = relationship(
        "Item",
        back_populates="user_items"
    )
