# Initialize wallets api
from fastapi import APIRouter
from app.api.endpoints import users, wallets, tg_bot_actions

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(wallets.router, prefix="/wallets", tags=["wallets"])
api_router.include_router(tg_bot_actions.router, prefix="/tg_bot_actions", tags=["tg_bot"])
