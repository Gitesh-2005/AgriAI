import json
from typing import Dict, List
from app.agents.base import BaseAgent, AgentResponse
from app.services.groq_service import GroqService

class CropAdvisoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Crop Advisory",
            description="Provides crop recommendations based on location, season, and soil conditions"
        )
        self.groq_service = GroqService()
        
        # Crop database with regional adaptations
        self.crop_database = {
            "rice": {
                "seasons": ["kharif", "rabi"],
                "soil_types": ["clay", "loam"],
                "water_requirements": "high",
                "growing_period": "120-150 days",
                "varieties": {
                    "north": ["Basmati", "PR-114", "Pusa-44"],
                    "south": ["Ponni", "ADT-43", "Samba Mahsuri"],
                    "east": ["Swarna", "Lalat", "Pooja"],
                    "west": ["Indrayani", "Ambemohar", "Kolam"]
                }
            },
            "wheat": {
                "seasons": ["rabi"],
                "soil_types": ["loam", "clay-loam"],
                "water_requirements": "medium",
                "growing_period": "120-140 days",
                "varieties": {
                    "north": ["PBW-343", "HD-2967", "WH-147"],
                    "central": ["GW-366", "MP-3288", "HI-1544"],
                    "south": ["DWR-162", "NIAW-34", "UAS-304"]
                }
            },
            "maize": {
                "seasons": ["kharif", "rabi", "summer"],
                "soil_types": ["well-drained loam"],
                "water_requirements": "medium",
                "growing_period": "90-120 days",
                "varieties": {
                    "north": ["Ganga-5", "HQPM-1", "Vivek-9"],
                    "south": ["NAC-6002", "COH-M5", "K-235"],
                    "west": ["Ganga-11", "Deccan-103", "Shaktiman-1"]
                }
            }
        }
    
    async def process(self, query: str, context: Dict = None) -> AgentResponse:
        """Process crop advisory queries"""
        
        # Extract location, season, and other factors from query
        location = self._extract_location(query, context)
        season = self._extract_season(query, context)
        soil_type = self._extract_soil_type(query, context)
        
        # Get crop recommendations
        recommendations = self._get_crop_recommendations(location, season, soil_type)
        
        # Use Groq for detailed advisory
        groq_prompt = f"""
        As an agricultural expert, provide detailed crop recommendations for:
        Location: {location}
        Season: {season}
        Soil Type: {soil_type}
        Query: {query}
        
        Base recommendations: {json.dumps(recommendations)}
        
        Provide specific advice on:
        1. Best crop varieties for this region and season
        2. Sowing dates and techniques
        3. Expected yield and market potential
        4. Risk factors and mitigation strategies
        5. Input requirements (seeds, fertilizers, water)
        
        Keep the response practical and actionable for farmers.
        """
        
        groq_response = await self.groq_service.generate_response(groq_prompt)
        
        return AgentResponse(
            agent_name=self.name,
            response=groq_response,
            confidence=0.85,
            metadata={
                "location": location,
                "season": season,
                "soil_type": soil_type,
                "recommended_crops": [crop["name"] for crop in recommendations],
                "analysis_factors": ["location", "season", "soil", "market_demand"]
            },
            citations=["ICAR Crop Production Guidelines", "State Agricultural Department"]
        )
    
    def _extract_location(self, query: str, context: Dict = None) -> str:
        """Extract location from query or context"""
        if context and context.get("location"):
            return context["location"]
        
        # Simple location extraction (can be enhanced with NER)
        import re
        location_pattern = r'\b(punjab|haryana|uttar pradesh|bihar|west bengal|maharashtra|karnataka|tamil nadu|andhra pradesh|telangana|gujarat|rajasthan|madhya pradesh|odisha|jharkhand|chhattisgarh|kerala|assam|himachal pradesh|uttarakhand)\b'
        match = re.search(location_pattern, query.lower())
        return match.group(1) if match else "general"
    
    def _extract_season(self, query: str, context: Dict = None) -> str:
        """Extract season from query"""
        import re
        season_pattern = r'\b(kharif|rabi|summer|monsoon|winter|rainy)\b'
        match = re.search(season_pattern, query.lower())
        if match:
            season = match.group(1)
            if season in ["monsoon", "rainy"]:
                return "kharif"
            elif season == "winter":
                return "rabi"
            return season
        
        # Default based on current month
        from datetime import datetime
        month = datetime.now().month
        if month in [6, 7, 8, 9, 10]:
            return "kharif"
        elif month in [11, 12, 1, 2, 3, 4]:
            return "rabi"
        else:
            return "summer"
    
    def _extract_soil_type(self, query: str, context: Dict = None) -> str:
        """Extract soil type from query or context"""
        if context and context.get("soil_type"):
            return context["soil_type"]
        
        import re
        soil_pattern = r'\b(clay|loam|sandy|silt|alluvial|black|red|laterite)\b'
        match = re.search(soil_pattern, query.lower())
        return match.group(1) if match else "loam"
    
    def _get_crop_recommendations(self, location: str, season: str, soil_type: str) -> List[Dict]:
        """Get crop recommendations based on parameters"""
        recommendations = []
        
        for crop_name, crop_info in self.crop_database.items():
            # Check season compatibility
            if season in crop_info["seasons"]:
                # Check soil compatibility
                if any(soil in crop_info["soil_types"] for soil in [soil_type, "well-drained " + soil_type]):
                    
                    # Get regional varieties
                    region = self._get_region(location)
                    varieties = crop_info["varieties"].get(region, crop_info["varieties"]["north"])
                    
                    recommendations.append({
                        "name": crop_name,
                        "suitability_score": self._calculate_suitability(crop_info, season, soil_type),
                        "varieties": varieties[:3],  # Top 3 varieties
                        "growing_period": crop_info["growing_period"],
                        "water_requirements": crop_info["water_requirements"]
                    })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        return recommendations[:5]  # Top 5 recommendations
    
    def _get_region(self, location: str) -> str:
        """Map location to region"""
        north_states = ["punjab", "haryana", "uttar pradesh", "bihar", "himachal pradesh", "uttarakhand"]
        south_states = ["karnataka", "tamil nadu", "andhra pradesh", "telangana", "kerala"]
        east_states = ["west bengal", "odisha", "jharkhand", "assam"]
        west_states = ["maharashtra", "gujarat", "rajasthan", "madhya pradesh", "chhattisgarh"]
        
        location_lower = location.lower()
        if any(state in location_lower for state in north_states):
            return "north"
        elif any(state in location_lower for state in south_states):
            return "south"
        elif any(state in location_lower for state in east_states):
            return "east"
        elif any(state in location_lower for state in west_states):
            return "west"
        else:
            return "north"  # default
    
    def _calculate_suitability(self, crop_info: Dict, season: str, soil_type: str) -> float:
        """Calculate crop suitability score"""
        score = 0.5  # base score
        
        # Season match
        if season in crop_info["seasons"]:
            score += 0.3
        
        # Soil match
        if soil_type in " ".join(crop_info["soil_types"]):
            score += 0.2
        
        return min(score, 1.0)