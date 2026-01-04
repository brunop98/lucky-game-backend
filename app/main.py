from fastapi import FastAPI
from app.core.database import engine
from app.core.version_middleware import VersionMiddleware
from app.models.base import Base
from app.api.router import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lucky Game Backend")
app.add_middleware(VersionMiddleware)
app.include_router(api_router)
