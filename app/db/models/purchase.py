from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.db.models.base import Base
from app.helpers.time_helper import utcnow


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    store = Column(String)  # google | apple
    product_id = Column(String)
    receipt_id = Column(String, unique=True)
    amount = Column(Integer)

    # timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow)
