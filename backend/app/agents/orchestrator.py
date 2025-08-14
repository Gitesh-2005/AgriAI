import asyncio
import json
from typing import Dict, List, Optional, Tuple
from app.agents.base import BaseAgent, AgentResponse
from app.agents.intent_classifier import IntentClassifierAgent
from app.agents.crop_advisory import CropAdvisoryAgent
from app.agents.weather import WeatherAgent
from app.agents.market_intelligence import MarketIntelligenceAgent
from app.agents.soil_analysis import SoilAnalysisAgent
from app.agents.pest_disease import PestDiseaseAgent
from app.agents.irrigation_planning import IrrigationPlanningAgent
from app.agents.financial_planning import FinancialPlanningAgent
from app.agents.policy_query import PolicyQueryAgent
from app.agents.translation import TranslationAgent
from app.agents.llm_chat import LLMChatAgent
from app.core.redis_client import redis_client

class AgentOrchestrator:
    def __init__(self):
        # Initialize all agents
        self.agents = {
            "intent_classifier": IntentClassifierAgent(),
            "crop_advisory": CropAdvisoryAgent(),
            "weather": WeatherAgent(),
            "market_intelligence": MarketIntelligenceAgent(),
            "soil_analysis": SoilAnalysisAgent(),
            "pest_disease": PestDiseaseAgent(),
            "irrigation_planning": IrrigationPlanningAgent(),
            "financial_planning": FinancialPlanningAgent(),
            "policy_query": PolicyQueryAgent(),
            "translation": TranslationAgent(),
            "llm_chat": LLMChatAgent(),
        }
        
        # Agent routing map
        self.intent_to_agent = {
            "crop_advisory": "crop_advisory",
            "soil_analysis": "soil_analysis",
            "weather": "weather",
            "irrigation": "irrigation_planning",
            "pest_disease": "pest_disease",
            "market_intelligence": "market_intelligence",
            "financial": "financial_planning",
            "policy": "policy_query",
            "translation": "translation",
            "general": "crop_advisory"  # Default to crop advisory
        }
    
    async def process_query(
        self, 
        query: str, 
        user_id: str, 
        session_id: str,
        context: Optional[Dict] = None
    ) -> AgentResponse:
        """Process a user query through the agent system"""
        try:
            # Step 1: Classify intent
            intent_response = await self.agents["intent_classifier"].process(query, context)
            primary_intent = intent_response.metadata.get("primary_intent", "general")
            
            # Step 2: Get user context from memory
            user_context = await self._get_user_context(user_id)
            if context:
                user_context.update(context)
            
            # Ensure conversation_history is present
            if "conversation_history" not in user_context:
                user_context["conversation_history"] = []
            
            # Step 3: Route to appropriate agent
            agent_name = self.intent_to_agent.get(primary_intent, "crop_advisory")
            agent = self.agents.get(agent_name)
            if not agent:
                agent = self.agents["crop_advisory"]
                agent_name = "crop_advisory"
            
            # Step 4: Process with selected agent
            response = await agent.process(query, user_context)
            
            # Step 5: Enhance response with context
            enhanced_response = await self._enhance_response(response, intent_response, user_context)
            
            # Step 6: Save conversation to memory
            # Update conversation_history
            user_context["conversation_history"].append({
                "user": query,
                "assistant": enhanced_response.response
            })
            # Keep only last 10 turns
            user_context["conversation_history"] = user_context["conversation_history"][-10:]
            await self._save_conversation(user_id, session_id, query, enhanced_response)
            
            # Save updated user_context with conversation_history
            context_key = f"user_context:{user_id}"
            await redis_client.setex(
                context_key, 
                3600 * 24 * 7,  # 7 days
                json.dumps(user_context)
            )
            
            return enhanced_response
            
        except Exception as e:
            # Error handling
            return AgentResponse(
                agent_name="System",
                response=f"I encountered an error while processing your query. Please try again or rephrase your question. Error: {str(e)}",
                confidence=0.1,
                metadata={"error": str(e), "fallback": True}
            )
    
    async def _get_user_context(self, user_id: str) -> Dict:
        """Retrieve user context from Redis"""
        try:
            context_key = f"user_context:{user_id}"
            context_data = await redis_client.get(context_key)
            return json.loads(context_data) if context_data else {}
        except Exception:
            return {}
    
    async def _save_conversation(
        self, 
        user_id: str, 
        session_id: str, 
        query: str, 
        response: AgentResponse
    ):
        """Save conversation to Redis for context"""
        try:
            # Save recent conversation
            conversation_key = f"conversation:{user_id}:{session_id}"
            conversation_data = {
                "query": query,
                "response": response.response,
                "agent": response.agent_name,
                "confidence": response.confidence,
                "timestamp": asyncio.get_event_loop().time()
            }
            
            # Keep last 10 conversations
            await redis_client.lpush(conversation_key, json.dumps(conversation_data))
            await redis_client.ltrim(conversation_key, 0, 9)
            await redis_client.expire(conversation_key, 3600 * 24)  # 24 hours
            
            # Update user context
            user_context = await self._get_user_context(user_id)
            
            # Extract and save relevant context from response
            if response.metadata:
                if "location" in response.metadata:
                    user_context["location"] = response.metadata["location"]
                if "commodity" in response.metadata:
                    user_context["last_commodity"] = response.metadata["commodity"]
                if "crop_types" in response.metadata:
                    user_context["crop_interests"] = response.metadata["crop_types"]
            
            # Save updated context
            context_key = f"user_context:{user_id}"
            await redis_client.setex(
                context_key, 
                3600 * 24 * 7,  # 7 days
                json.dumps(user_context)
            )
            
        except Exception as e:
            print(f"Error saving conversation: {e}")
    
    async def _enhance_response(
        self, 
        response: AgentResponse, 
        intent_response: AgentResponse,
        user_context: Dict
    ) -> AgentResponse:
        """Enhance response with additional context and recommendations"""
        
        enhanced_response = response.response
        
        # Add contextual information
        if user_context.get("location"):
            location = user_context["location"]
            if location.lower() not in enhanced_response.lower():
                enhanced_response += f"\n\n*Note: This advice is tailored for {location} region.*"
        
        # Add follow-up suggestions based on intent
        primary_intent = intent_response.metadata.get("primary_intent")
        
        follow_ups = {
            "crop_advisory": [
                "Would you like weather information for your area?",
                "Do you need market price information for this crop?",
                "Would you like soil preparation advice?"
            ],
            "weather": [
                "Would you like irrigation scheduling advice?",
                "Do you need crop protection recommendations?",
                "Would you like to know about suitable crops for this weather?"
            ],
            "market_intelligence": [
                "Would you like crop advisory for better profits?",
                "Do you need information about storage and transportation?",
                "Would you like to know about government schemes?"
            ]
        }
        
        if primary_intent in follow_ups:
            suggestions = follow_ups[primary_intent][:2]  # Top 2 suggestions
            enhanced_response += f"\n\n**Related Questions:**\n"
            for suggestion in suggestions:
                enhanced_response += f"• {suggestion}\n"
        
        # Create enhanced response object
        enhanced = AgentResponse(
            agent_name=response.agent_name,
            response=enhanced_response,
            confidence=response.confidence,
            metadata={
                **response.metadata,
                "intent_confidence": intent_response.confidence,
                "primary_intent": primary_intent,
                "user_context_used": bool(user_context)
            },
            citations=response.citations,
            requires_followup=len(follow_ups.get(primary_intent, [])) > 0
        )
        
        return enhanced
    
    async def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all agents"""
        capabilities = {}
        for name, agent in self.agents.items():
            capabilities[name] = {
                "description": agent.description,
                "capabilities": agent.capabilities
            }
        return capabilities
    
    async def health_check(self) -> Dict[str, str]:
        """Check health of all agents"""
        health = {}
        for name, agent in self.agents.items():
            try:
                # Simple health check - try to process a basic query
                test_response = await agent.process("health check", {})
                health[name] = "healthy" if test_response else "unhealthy"
            except Exception as e:
                health[name] = f"error: {str(e)}"
        return health
    
    async def route(self, query: str, context: dict = None) -> dict:
        # For now, always use LLMChatAgent (or you can add intent logic)
        agent = self.agents["llm_chat"]
        response = await agent.process(query, context)
        return response.dict()