from fastapi import APIRouter, Depends
from typing import Dict, List
from app.agents.orchestrator import AgentOrchestrator

router = APIRouter()

# Initialize orchestrator
orchestrator = AgentOrchestrator()

@router.get("/capabilities")
async def get_agent_capabilities() -> Dict[str, Dict]:
    """Get capabilities of all available agents"""
    return await orchestrator.get_agent_capabilities()

@router.get("/health")
async def check_agent_health() -> Dict[str, str]:
    """Check health status of all agents"""
    return await orchestrator.health_check()

@router.get("/list")
async def list_agents() -> Dict[str, List[str]]:
    """List all available agents"""
    capabilities = await orchestrator.get_agent_capabilities()
    return {
        "agents": list(capabilities.keys()),
        "total_count": len(capabilities),
        "descriptions": {name: info["description"] for name, info in capabilities.items()}
    }