import re
from typing import Dict, List, Tuple
from app.agents.base import BaseAgent, AgentResponse

class IntentClassifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Intent Classifier",
            description="Classifies natural language queries into agricultural domains"
        )
        
        # Intent patterns with confidence weights
        self.intent_patterns = {
            "crop_advisory": [
                (r"\b(crop|plant|seed|variety|sowing|harvest)\b", 0.8),
                (r"\b(which crop|what to grow|best crop|recommend crop)\b", 0.9),
                (r"\b(season|timing|when to plant)\b", 0.7),
            ],
            "soil_analysis": [
                (r"\b(soil|pH|nitrogen|phosphorus|potassium|NPK|nutrients)\b", 0.8),
                (r"\b(soil test|soil health|soil quality)\b", 0.9),
                (r"\b(fertilizer|manure|compost)\b", 0.6),
            ],
            "weather": [
                (r"\b(weather|rain|temperature|humidity|wind)\b", 0.8),
                (r"\b(forecast|climate|monsoon|drought)\b", 0.7),
                (r"\b(will it rain|weather today|temperature)\b", 0.9),
            ],
            "irrigation": [
                (r"\b(water|irrigation|watering|moisture)\b", 0.8),
                (r"\b(drip|sprinkler|flood irrigation)\b", 0.9),
                (r"\b(when to water|how much water)\b", 0.8),
            ],
            "pest_disease": [
                (r"\b(pest|disease|insect|fungus|virus|bacteria)\b", 0.8),
                (r"\b(leaf spot|blight|aphid|caterpillar)\b", 0.9),
                (r"\b(plant sick|leaves turning|crop damage)\b", 0.7),
            ],
            "market_intelligence": [
                (r"\b(price|market|mandi|sell|buy)\b", 0.8),
                (r"\b(commodity|trading|auction)\b", 0.7),
                (r"\b(market rate|current price|price trend)\b", 0.9),
            ],
            "financial": [
                (r"\b(loan|credit|subsidy|insurance|EMI)\b", 0.8),
                (r"\b(bank|finance|money|cost|profit)\b", 0.6),
                (r"\b(PM-Kisan|crop insurance|KCC)\b", 0.9),
            ],
            "policy": [
                (r"\b(policy|government|scheme|law|regulation)\b", 0.8),
                (r"\b(MSP|procurement|support price)\b", 0.9),
                (r"\b(eligibility|application|form)\b", 0.6),
            ]
        }
    
    async def process(self, query: str, context: Dict = None) -> AgentResponse:
        """Classify the intent of a query"""
        query_lower = query.lower()
        intent_scores = {}
        
        # Calculate scores for each intent
        for intent, patterns in self.intent_patterns.items():
            score = 0.0
            matches = []
            
            for pattern, weight in patterns:
                if re.search(pattern, query_lower):
                    score += weight
                    matches.append(pattern)
            
            if score > 0:
                intent_scores[intent] = {
                    "score": min(score, 1.0),  # Cap at 1.0
                    "matches": matches
                }
        
        # Find the best intent
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1]["score"])
            primary_intent = best_intent[0]
            confidence = best_intent[1]["score"]
        else:
            primary_intent = "general"
            confidence = 0.5
        
        return AgentResponse(
            agent_name=self.name,
            response=f"Classified as: {primary_intent}",
            confidence=confidence,
            metadata={
                "primary_intent": primary_intent,
                "all_intents": intent_scores,
                "query_length": len(query)
            }
        )