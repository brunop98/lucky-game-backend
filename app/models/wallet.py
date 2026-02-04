from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    xp = Column(Integer, default=0)
    coins = Column(Integer, default=0)
    gems = Column(Integer, default=0)
    energy = Column(Integer, default=0)

    last_energy_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    
    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="wallet")



# TODO RECOMPENSA DE AD
# o que eu recebo

# qual_item_clicou_para_ganhar
# se_assistiu_o_ad_inteiro

# O que eu retorno
# Lista_de_items_para_ganhar