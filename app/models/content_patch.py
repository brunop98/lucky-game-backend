from sqlalchemy import Boolean, Column, Integer, String
from app.models.base import Base

class ContentPatch(Base):
    __tablename__ = "content_patches"

    id = Column(Integer, primary_key=True)
    app_version_min = Column(String, nullable=False)
    app_version_max = Column(String, nullable=False)

    content_version = Column(String, nullable=False)

    catalog_url = Column(String, nullable=False)
    base_url = Column(String, nullable=False)

    size_mb = Column(Integer, nullable=False)
    mandatory = Column(Boolean, default=False)
    checksum = Column(String, nullable=True) 

    active = Column(Boolean, default=False)
