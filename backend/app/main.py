from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.api.routes import api_router
from app.core.database import engine, Base
from app.core.redis_client import redis_client

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🌱 Agriculture AI System Starting...")
    try:
        # Test Redis connection
        await redis_client.ping()
        print("✅ Redis connected successfully")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
    
    yield
    
    # Shutdown
    print("🌾 Agriculture AI System Shutting down...")
    await redis_client.close()

app = FastAPI(
    title="Agriculture AI System",
    description="Agentic AI system for agricultural decision-making",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Agriculture AI System API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    try:
        await redis_client.ping()
        return {
            "status": "healthy",
            "redis": "connected",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )