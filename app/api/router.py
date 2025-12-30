from fastapi import APIRouter

from app.api.cards_routes import router as cards_router
from app.api.auth_routes import router as auth_router
from app.api.wallet_routes import router as wallet_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(wallet_router)
api_router.include_router(cards_router)
