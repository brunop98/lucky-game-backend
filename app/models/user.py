from sqlalchemy import Column, Integer, String
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Auth
    auth_provider = Column(String, nullable=False, index=True)  
    provider_user_id = Column(String, nullable=False, index=True)

    # Profile
    email = Column(String, nullable=True, index=True)
    full_name = Column(String, nullable=False)
    locale = Column(String, nullable=True)
    picture_url = Column(String, nullable=True)

    __table_args__ = (
        # garante unicidade por provider
        {"sqlite_autoincrement": True},
    )
