from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.api.endpoints.auth import get_current_user
from app.models.user import User
from app.models.conversation import Conversation
from app.agents.orchestrator import AgentOrchestrator

router = APIRouter()

# Initialize orchestrator
orchestrator = AgentOrchestrator()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    language: str = "en"

class ChatResponse(BaseModel):
    response: str
    agent_used: str
    confidence: float
    session_id: str
    metadata: Dict[str, Any]
    citations: list
    requires_followup: bool

@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to the AI system and get a response"""
    
    # Generate session ID if not provided
    session_id = chat_request.session_id or str(uuid.uuid4())
    
    # Add user context
    user_context = {
        "user_id": current_user.id,
        "user_type": current_user.user_type,
        "location": current_user.location,
        "language": current_user.language_preference,
        "farm_size": current_user.farm_size
    }
    
    # Merge with provided context
    if chat_request.context:
        user_context.update(chat_request.context)
    
    try:
        # Process the query through the orchestrator
        agent_response = await orchestrator.process_query(
            query=chat_request.message,
            user_id=str(current_user.id),
            session_id=session_id,
            context=user_context
        )
        
        # Save conversation to database
        conversation = Conversation(
            user_id=current_user.id,
            session_id=session_id,
            query=chat_request.message,
            response=agent_response.response,
            agent_used=agent_response.agent_name,
            intent=agent_response.metadata.get("primary_intent", "unknown"),
            confidence_score=agent_response.confidence,
            language=chat_request.language,
            metadata=str(agent_response.metadata)
        )
        
        db.add(conversation)
        db.commit()
        
        return ChatResponse(
            response=agent_response.response,
            agent_used=agent_response.agent_name,
            confidence=agent_response.confidence,
            session_id=session_id,
            metadata=agent_response.metadata,
            citations=agent_response.citations,
            requires_followup=agent_response.requires_followup
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history for a session"""
    
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.session_id == session_id
    ).order_by(Conversation.created_at.desc()).limit(50).all()
    
    return [
        {
            "id": conv.id,
            "query": conv.query,
            "response": conv.response,
            "agent_used": conv.agent_used,
            "confidence": conv.confidence_score,
            "created_at": conv.created_at,
            "intent": conv.intent
        }
        for conv in conversations
    ]

@router.get("/sessions")
async def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all chat sessions for the current user"""
    
    sessions = db.query(Conversation.session_id, Conversation.created_at).filter(
        Conversation.user_id == current_user.id
    ).distinct().order_by(Conversation.created_at.desc()).limit(20).all()
    
    return [
        {
            "session_id": session.session_id,
            "last_activity": session.created_at
        }
        for session in sessions
    ]