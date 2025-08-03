from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./agri_ai.db"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # JWT
    secret_key: str = "your-super-secret-jwt-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Groq API
    groq_api_key: Optional[str] = None
    
    # Weather API
    weather_api_key: Optional[str] = None
    
    # External APIs
    agmarknet_api_url: str = "https://enam.gov.in/web/"
    imd_api_url: str = "https://mausam.imd.gov.in/"
    
    class Config:
        env_file = ".env"

settings = Settings()