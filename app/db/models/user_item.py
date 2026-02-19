from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.helpers.time_helper import utcnow


class UserItem(Base):
    __tablename__ = "user_items"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    stack_size = Column(Integer, nullable=False, default=1)

    # timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow)

    __table_args__ = (
        CheckConstraint("stack_size > 0", name="ck_cards_stack_size_positive"),
        {"sqlite_autoincrement": True},
    )

    user = relationship("User", back_populates="user_item")

    item = relationship("Item", back_populates="user_item")
