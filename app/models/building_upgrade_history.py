from locale import currency
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.helpers.time_helper import utcnow
from app.models.base import Base


class BuildingUpgradeHistory(Base):
    __tablename__ = "building_upgrade_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    village_id = Column(Integer, ForeignKey("villages.id")) 
    building_id = Column(Integer, ForeignKey("buildings.id"))
    new_building_stage = Column(Integer)

    # timestamps
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow)

    user = relationship("User", back_populates="building_upgrade_history") 
    village = relationship("Villages", back_populates="building_upgrade_history")
    building = relationship("Building", back_populates="building_upgrade_history") 


    __table_args__ = (
        # garante unicidade por provider
        {"sqlite_autoincrement": True},
    )
