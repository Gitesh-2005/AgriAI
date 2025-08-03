from fastapi import APIRouter
from app.api.endpoints import auth, agents, chat

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])