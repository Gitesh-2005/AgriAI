from fastapi import APIRouter
from app.api.endpoints import auth, agents, chat, tts, stt, open_meteo

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(tts.router, tags=["text-to-speech"])  
api_router.include_router(stt.router, prefix="/stt", tags=["audio processing"])
api_router.include_router(open_meteo.router, prefix="/weather", tags=["weather"])
