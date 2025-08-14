import os
from groq import Groq
from dotenv import load_dotenv
from .base import BaseAgent, AgentResponse

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env.")

groq_client = Groq(api_key=api_key)

class LLMChatAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="LLMChatAgent",
            description="Conversational agent for AgriAI that can greet, answer farming queries, and maintain context."
        )
        self.add_capability("conversation")
        self.add_capability("farming_qna")

    async def process(self, query: str, context: dict = None) -> AgentResponse:
        # Check conversation context
        if not context or "conversation_history" not in context:
            user_name = context.get("full_name") if context else None
            greeting = f"👋 Hello{f' {user_name}' if user_name else ''}! I’m your AgriAI assistant. I can share crop prices, give farming tips, and help you decide what to plant. How can I help today?"
            return AgentResponse(
                agent_name=self.name,
                response=greeting,
                confidence=1.0,
                metadata={"type": "greeting"},
                requires_followup=True
            )

        # Build prompt with conversation history
        history_text = ""
        for turn in context["conversation_history"][-5:]:  # last 5 messages
            history_text += f"User: {turn['user']}\nAI: {turn['assistant']}\n"

        prompt = f"""
You are AgriAI, a multilingual AI assistant for farmers.
You can answer questions about crop prices, farming tips, weather, and crop selection.
Respond clearly and simply.

Conversation so far:
{history_text}

User's new message:
{query}
"""

        # Call Groq LLM
        completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",  # or your preferred Groq chat model
            messages=[
                {"role": "system", "content": "You are AgriAI, a helpful farming assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        answer = completion.choices[0].message.content

        return AgentResponse(
            agent_name=self.name,
            response=answer,
            confidence=0.95,
            metadata={"type": "llm_response"},
            requires_followup=True
        )

    async def can_handle(self, intent: str, query: str) -> float:
        # Let LLM handle almost all conversational queries
        return 0.85
