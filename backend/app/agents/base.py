from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from pydantic import BaseModel
import json
import asyncio
from datetime import datetime

class AgentResponse(BaseModel):
    agent_name: str
    response: str
    confidence: float
    metadata: Dict[str, Any] = {}
    citations: List[str] = []
    requires_followup: bool = False
    
class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.capabilities = []
        
    @abstractmethod
    async def process(self, query: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process a query and return a response"""
        pass
    
    async def can_handle(self, intent: str, query: str) -> float:
        """Return confidence score (0-1) for handling this query"""
        return 0.0
    
    def add_capability(self, capability: str):
        """Add a capability to this agent"""
        self.capabilities.append(capability)
    
    async def get_memory_context(self, user_id: str, redis_client) -> Dict[str, Any]:
        """Retrieve user context from memory"""
        try:
            context_key = f"user_context:{user_id}"
            context_data = await redis_client.get(context_key)
            return json.loads(context_data) if context_data else {}
        except Exception:
            return {}
    
    async def save_memory_context(self, user_id: str, context: Dict[str, Any], redis_client):
        """Save user context to memory"""
        try:
            context_key = f"user_context:{user_id}"
            await redis_client.setex(
                context_key, 
                3600 * 24,  # 24 hours
                json.dumps(context)
            )
        except Exception:
            pass