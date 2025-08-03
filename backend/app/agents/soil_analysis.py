import json
from typing import Dict, List
from app.agents.base import BaseAgent, AgentResponse
from app.services.groq_service import GroqService

class SoilAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Soil Analysis",
            description="Analyzes soil health and provides fertilizer recommendations"
        )
        self.groq_service = GroqService()
        
        # Soil type characteristics
        self.soil_types = {
            "clay": {
                "characteristics": ["High water retention", "Poor drainage", "Rich in nutrients"],
                "suitable_crops": ["Rice", "Wheat", "Cotton"],
                "ph_range": "6.0-7.5",
                "drainage": "poor",
                "fertility": "high"
            },
            "sandy": {
                "characteristics": ["Good drainage", "Low water retention", "Low nutrients"],
                "suitable_crops": ["Groundnut", "Watermelon", "Carrot"],
                "ph_range": "6.0-7.0",
                "drainage": "excellent",
                "fertility": "low"
            },
            "loam": {
                "characteristics": ["Balanced drainage", "Good water retention", "Fertile"],
                "suitable_crops": ["Most crops", "Vegetables", "Fruits"],
                "ph_range": "6.0-7.0",
                "drainage": "good",
                "fertility": "high"
            },
            "black": {
                "characteristics": ["High clay content", "Rich in nutrients", "Good for cotton"],
                "suitable_crops": ["Cotton", "Sugarcane", "Soybean"],
                "ph_range": "7.0-8.5",
                "drainage": "moderate",
                "fertility": "very high"
            }
        }
        
        # NPK recommendations by crop
        self.npk_recommendations = {
            "rice": {"N": 120, "P": 60, "K": 40, "timing": "Split application"},
            "wheat": {"N": 120, "P": 60, "K": 40, "timing": "Basal + top dressing"},
            "cotton": {"N": 120, "P": 60, "K": 60, "timing": "Multiple splits"},
            "sugarcane": {"N": 280, "P": 92, "K": 140, "timing": "Multiple applications"},
            "maize": {"N": 120, "P": 60, "K": 40, "timing": "Split application"}
        }
    
    async def process(self, query: str, context: Dict = None) -> AgentResponse:
        """Process soil analysis queries"""
        
        # Extract soil parameters from query
        soil_type = self._extract_soil_type(query, context)
        crop_type = self._extract_crop_type(query, context)
        ph_level = self._extract_ph_level(query)
        
        # Generate soil analysis report
        analysis = self._analyze_soil(soil_type, crop_type, ph_level)
        
        # Get fertilizer recommendations
        fertilizer_rec = self._get_fertilizer_recommendations(crop_type, soil_type, analysis)
        
        # Use Groq for detailed recommendations
        groq_prompt = f"""
        As a soil scientist, provide detailed soil management advice for:
        
        Soil Type: {soil_type}
        Crop: {crop_type}
        pH Level: {ph_level}
        Analysis: {json.dumps(analysis)}
        
        Provide specific recommendations for:
        1. Soil health improvement strategies
        2. Organic matter enhancement
        3. Nutrient management plan
        4. pH correction methods if needed
        5. Sustainable farming practices
        
        Include specific quantities, timing, and application methods.
        """
        
        groq_response = await self.groq_service.generate_response(groq_prompt)
        
        # Format comprehensive response
        response_text = self._format_soil_response(analysis, fertilizer_rec, groq_response)
        
        return AgentResponse(
            agent_name=self.name,
            response=response_text,
            confidence=0.88,
            metadata={
                "soil_type": soil_type,
                "crop_type": crop_type,
                "ph_level": ph_level,
                "fertility_status": analysis.get("fertility_status"),
                "recommendations": fertilizer_rec
            },
            citations=["Soil Health Card Scheme", "ICAR Guidelines", "State Agricultural Universities"]
        )
    
    def _extract_soil_type(self, query: str, context: Dict = None) -> str:
        """Extract soil type from query or context"""
        if context and context.get("soil_type"):
            return context["soil_type"]
        
        query_lower = query.lower()
        for soil_type in self.soil_types.keys():
            if soil_type in query_lower:
                return soil_type
        
        return "loam"  # Default
    
    def _extract_crop_type(self, query: str, context: Dict = None) -> str:
        """Extract crop type from query"""
        query_lower = query.lower()
        crops = ["rice", "wheat", "cotton", "sugarcane", "maize", "soybean", "groundnut"]
        
        for crop in crops:
            if crop in query_lower:
                return crop
        
        return "general"
    
    def _extract_ph_level(self, query: str) -> str:
        """Extract pH level from query"""
        import re
        ph_match = re.search(r'ph\s*(\d+\.?\d*)', query.lower())
        if ph_match:
            return ph_match.group(1)
        return "unknown"
    
    def _analyze_soil(self, soil_type: str, crop_type: str, ph_level: str) -> Dict:
        """Analyze soil conditions"""
        analysis = {
            "soil_type": soil_type,
            "characteristics": self.soil_types.get(soil_type, {}).get("characteristics", []),
            "drainage": self.soil_types.get(soil_type, {}).get("drainage", "unknown"),
            "fertility_status": self.soil_types.get(soil_type, {}).get("fertility", "unknown"),
            "suitable_crops": self.soil_types.get(soil_type, {}).get("suitable_crops", []),
            "ph_analysis": self._analyze_ph(ph_level),
            "crop_suitability": self._check_crop_suitability(soil_type, crop_type)
        }
        
        return analysis
    
    def _analyze_ph(self, ph_level: str) -> Dict:
        """Analyze pH level"""
        if ph_level == "unknown":
            return {"status": "unknown", "recommendation": "Get soil pH tested"}
        
        try:
            ph = float(ph_level)
            if ph < 6.0:
                return {
                    "status": "acidic",
                    "recommendation": "Apply lime to increase pH",
                    "severity": "high" if ph < 5.5 else "moderate"
                }
            elif ph > 8.0:
                return {
                    "status": "alkaline",
                    "recommendation": "Apply gypsum or sulfur to reduce pH",
                    "severity": "high" if ph > 8.5 else "moderate"
                }
            else:
                return {
                    "status": "optimal",
                    "recommendation": "pH is in good range",
                    "severity": "none"
                }
        except:
            return {"status": "invalid", "recommendation": "Invalid pH value"}
    
    def _check_crop_suitability(self, soil_type: str, crop_type: str) -> Dict:
        """Check if crop is suitable for soil type"""
        if crop_type == "general":
            return {"suitable": True, "score": 0.7}
        
        suitable_crops = self.soil_types.get(soil_type, {}).get("suitable_crops", [])
        crop_suitable = any(crop_type.lower() in crop.lower() for crop in suitable_crops)
        
        return {
            "suitable": crop_suitable,
            "score": 0.9 if crop_suitable else 0.4,
            "alternative_crops": suitable_crops if not crop_suitable else []
        }
    
    def _get_fertilizer_recommendations(self, crop_type: str, soil_type: str, analysis: Dict) -> Dict:
        """Get fertilizer recommendations"""
        if crop_type in self.npk_recommendations:
            base_rec = self.npk_recommendations[crop_type].copy()
            
            # Adjust based on soil fertility
            fertility = analysis.get("fertility_status", "medium")
            if fertility == "low":
                base_rec["N"] = int(base_rec["N"] * 1.2)
                base_rec["P"] = int(base_rec["P"] * 1.3)
                base_rec["K"] = int(base_rec["K"] * 1.1)
            elif fertility == "high":
                base_rec["N"] = int(base_rec["N"] * 0.8)
                base_rec["P"] = int(base_rec["P"] * 0.9)
            
            return base_rec
        
        return {
            "N": 100, "P": 50, "K": 50,
            "timing": "Split application recommended"
        }
    
    def _format_soil_response(self, analysis: Dict, fertilizer_rec: Dict, groq_response: str) -> str:
        """Format comprehensive soil analysis response"""
        
        response = "🌱 **Soil Analysis Report**\n\n"
        
        # Soil characteristics
        response += f"**Soil Type:** {analysis['soil_type'].title()}\n"
        response += f"**Fertility Status:** {analysis['fertility_status'].title()}\n"
        response += f"**Drainage:** {analysis['drainage'].title()}\n\n"
        
        # pH analysis
        ph_analysis = analysis.get("ph_analysis", {})
        if ph_analysis.get("status") != "unknown":
            response += f"**pH Analysis:**\n"
            response += f"• Status: {ph_analysis['status'].title()}\n"
            response += f"• Recommendation: {ph_analysis['recommendation']}\n\n"
        
        # Crop suitability
        crop_suit = analysis.get("crop_suitability", {})
        if crop_suit.get("suitable"):
            response += f"✅ **Crop Suitability:** Good match for selected crop\n\n"
        else:
            response += f"⚠️ **Crop Suitability:** Consider alternative crops\n"
            if crop_suit.get("alternative_crops"):
                response += f"**Recommended crops:** {', '.join(crop_suit['alternative_crops'])}\n\n"
        
        # Fertilizer recommendations
        response += f"**Fertilizer Recommendations (per acre):**\n"
        response += f"• Nitrogen (N): {fertilizer_rec.get('N', 'N/A')} kg\n"
        response += f"• Phosphorus (P): {fertilizer_rec.get('P', 'N/A')} kg\n"
        response += f"• Potassium (K): {fertilizer_rec.get('K', 'N/A')} kg\n"
        response += f"• Application: {fertilizer_rec.get('timing', 'As per crop requirement')}\n\n"
        
        # Add Groq detailed recommendations
        response += f"**Detailed Recommendations:**\n{groq_response}"
        
        return response