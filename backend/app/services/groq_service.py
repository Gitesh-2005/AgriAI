import os
from typing import Dict, List, Optional
import json
from groq import Groq
from app.core.config import settings

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None
        self.model = "mixtral-8x7b-32768"  # Fast model for agricultural queries
        
    async def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate response using Groq API"""
        
        if not self.client:
            return self._get_fallback_response(prompt)
        
        try:
            # Prepare system message for agricultural context
            system_message = """You are an expert agricultural advisor with deep knowledge of:
            - Crop cultivation and farming practices
            - Soil health and fertilizer management
            - Weather impacts on agriculture
            - Market trends and pricing
            - Government schemes and subsidies
            - Pest and disease management
            - Irrigation and water management
            
            Provide practical, actionable advice that farmers can implement. 
            Use simple language and avoid overly technical jargon.
            Include specific recommendations with quantities, timing, and methods where applicable.
            Consider Indian agricultural context and practices.
            """
            
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
            
            # Add context if provided
            if context:
                context_str = f"Additional context: {json.dumps(context)}"
                messages.insert(-1, {"role": "user", "content": context_str})
            
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=1024,
                temperature=0.7,
                top_p=0.9
            )
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            print(f"Groq API error: {e}")
            return self._get_fallback_response(prompt)
    
    async def analyze_intent(self, query: str) -> Dict[str, float]:
        """Use Groq to analyze query intent"""
        
        if not self.client:
            return {"general": 0.5}
        
        try:
            prompt = f"""
            Analyze the following agricultural query and classify it into these categories with confidence scores (0-1):
            
            Categories:
            - crop_advisory: Questions about what crops to grow, varieties, planting advice
            - soil_analysis: Questions about soil health, nutrients, pH, fertilizers
            - weather: Weather forecasts, climate impact on crops
            - irrigation: Water management, irrigation schedules
            - pest_disease: Plant diseases, pest control, crop protection
            - market_intelligence: Prices, market trends, selling advice
            - financial: Loans, subsidies, insurance, cost analysis
            - policy: Government schemes, regulations, support programs
            
            Query: "{query}"
            
            Respond in JSON format only:
            {{"category": "primary_category", "confidence": 0.0, "secondary": "secondary_category"}}
            """
            
            response = await self.generate_response(prompt)
            
            try:
                result = json.loads(response)
                return {result["category"]: result["confidence"]}
            except:
                return {"general": 0.5}
                
        except Exception as e:
            print(f"Intent analysis error: {e}")
            return {"general": 0.5}
    
    def _get_fallback_response(self, prompt: str) -> str:
        """Fallback response when Groq API is not available"""
        
        # Simple keyword-based responses
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["crop", "plant", "grow", "variety"]):
            return """For crop selection, consider these factors:
            
            1. **Season**: Choose crops suitable for current season (Kharif/Rabi/Summer)
            2. **Soil**: Match crop requirements with your soil type
            3. **Water**: Consider irrigation availability
            4. **Market**: Check local demand and prices
            5. **Climate**: Ensure crops are suitable for your region
            
            Popular options:
            - **Kharif**: Rice, Cotton, Sugarcane, Maize
            - **Rabi**: Wheat, Barley, Gram, Mustard
            - **Summer**: Fodder crops, Vegetables
            
            Consult your local agriculture extension officer for specific recommendations."""
        
        elif any(word in prompt_lower for word in ["weather", "rain", "temperature"]):
            return """Weather information is crucial for farming decisions:
            
            **Current Recommendations**:
            - Monitor weather forecasts daily
            - Plan irrigation based on rainfall predictions
            - Protect crops during extreme weather
            - Adjust fertilizer application timing
            
            **General Advice**:
            - Use IMD weather forecasts
            - Follow agro-meteorological advisories
            - Install rain gauges for local measurement
            - Consider weather-indexed insurance
            
            For specific weather data, please provide your location."""
        
        elif any(word in prompt_lower for word in ["price", "market", "sell", "mandi"]):
            return """Market intelligence is key for profitable farming:
            
            **Price Information Sources**:
            - AgMarkNet portal for daily prices
            - eNAM platform for online trading
            - Local mandi rates
            - Commodity exchanges
            
            **Marketing Tips**:
            - Compare prices across multiple markets
            - Consider transportation costs
            - Time your sales based on market trends
            - Use futures contracts for price discovery
            
            **Government Support**:
            - MSP (Minimum Support Price) schemes
            - Market intervention schemes
            - Direct procurement centers"""
        
        else:
            return """I'd be happy to help with your agricultural query. For more specific assistance, please provide details about:
            
            - Your location/state
            - Type of farming (crops/livestock)
            - Specific concern or question
            - Current season/timing
            
            I can help with:
            ✅ Crop selection and varieties
            ✅ Soil health and fertilizers
            ✅ Weather and irrigation advice
            ✅ Market prices and trends
            ✅ Government schemes and subsidies
            ✅ Pest and disease management
            
            Please rephrase your question with more specific details."""