import json
from datetime import datetime, timedelta
from typing import Dict, List
from app.agents.base import BaseAgent, AgentResponse
from app.services.groq_service import GroqService

class IrrigationPlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Irrigation Planning",
            description="Provides irrigation scheduling and water management recommendations"
        )
        self.groq_service = GroqService()
        
        # Crop water requirements (mm per day during different stages)
        self.crop_water_requirements = {
            "rice": {
                "initial": 5.0,
                "development": 7.0,
                "mid_season": 8.5,
                "late_season": 4.0,
                "total_season": 1200,  # mm
                "critical_stages": ["Tillering", "Panicle initiation", "Flowering"]
            },
            "wheat": {
                "initial": 2.5,
                "development": 4.0,
                "mid_season": 5.5,
                "late_season": 2.0,
                "total_season": 450,
                "critical_stages": ["Crown root initiation", "Jointing", "Flowering"]
            },
            "cotton": {
                "initial": 3.0,
                "development": 5.0,
                "mid_season": 7.0,
                "late_season": 4.5,
                "total_season": 800,
                "critical_stages": ["Squaring", "Flowering", "Boll development"]
            },
            "maize": {
                "initial": 3.0,
                "development": 5.0,
                "mid_season": 6.5,
                "late_season": 3.5,
                "total_season": 500,
                "critical_stages": ["Tasseling", "Silking", "Grain filling"]
            },
            "sugarcane": {
                "initial": 4.0,
                "development": 6.0,
                "mid_season": 8.0,
                "late_season": 5.0,
                "total_season": 1800,
                "critical_stages": ["Tillering", "Grand growth", "Maturity"]
            }
        }
        
        # Irrigation methods efficiency
        self.irrigation_methods = {
            "flood": {"efficiency": 0.4, "water_saving": 0, "cost": "low"},
            "furrow": {"efficiency": 0.6, "water_saving": 0.3, "cost": "low"},
            "sprinkler": {"efficiency": 0.75, "water_saving": 0.5, "cost": "medium"},
            "drip": {"efficiency": 0.9, "water_saving": 0.7, "cost": "high"},
            "micro_sprinkler": {"efficiency": 0.8, "water_saving": 0.6, "cost": "medium"}
        }
    
    async def process(self, query: str, context: Dict = None) -> AgentResponse:
        """Process irrigation planning queries"""
        
        # Extract parameters from query
        crop = self._extract_crop(query, context)
        growth_stage = self._extract_growth_stage(query)
        soil_type = self._extract_soil_type(query, context)
        weather_condition = self._extract_weather_condition(query)
        irrigation_method = self._extract_irrigation_method(query)
        
        # Calculate irrigation requirements
        irrigation_plan = self._calculate_irrigation_plan(
            crop, growth_stage, soil_type, weather_condition, irrigation_method
        )
        
        # Use Groq for detailed irrigation advice
        groq_prompt = f"""
        As an irrigation specialist, provide comprehensive water management advice for:
        
        Crop: {crop}
        Growth Stage: {growth_stage}
        Soil Type: {soil_type}
        Weather: {weather_condition}
        Irrigation Method: {irrigation_method}
        
        Current irrigation plan: {json.dumps(irrigation_plan)}
        
        Provide specific guidance on:
        1. Optimal irrigation scheduling
        2. Water application rates and timing
        3. Soil moisture monitoring techniques
        4. Water conservation strategies
        5. Irrigation system maintenance
        6. Adjustments for weather conditions
        
        Include practical tips for efficient water use and cost savings.
        """
        
        groq_response = await self.groq_service.generate_response(groq_prompt)
        
        # Format response
        response_text = self._format_irrigation_response(irrigation_plan, groq_response)
        
        return AgentResponse(
            agent_name=self.name,
            response=response_text,
            confidence=0.87,
            metadata={
                "crop": crop,
                "growth_stage": growth_stage,
                "daily_water_need": irrigation_plan.get("daily_requirement"),
                "irrigation_frequency": irrigation_plan.get("frequency"),
                "water_efficiency": irrigation_plan.get("efficiency"),
                "cost_category": irrigation_plan.get("cost_category")
            },
            citations=["FAO Irrigation Guidelines", "ICAR Water Management", "State Irrigation Departments"]
        )
    
    def _extract_crop(self, query: str, context: Dict = None) -> str:
        """Extract crop from query or context"""
        if context and context.get("crop_type"):
            return context["crop_type"]
        
        query_lower = query.lower()
        for crop in self.crop_water_requirements.keys():
            if crop in query_lower:
                return crop
        
        return "general"
    
    def _extract_growth_stage(self, query: str) -> str:
        """Extract growth stage from query"""
        query_lower = query.lower()
        
        stage_keywords = {
            "initial": ["initial", "germination", "emergence", "seedling"],
            "development": ["development", "vegetative", "tillering", "branching"],
            "mid_season": ["flowering", "reproductive", "tasseling", "silking", "mid"],
            "late_season": ["maturity", "ripening", "harvest", "late", "grain filling"]
        }
        
        for stage, keywords in stage_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return stage
        
        return "development"  # Default
    
    def _extract_soil_type(self, query: str, context: Dict = None) -> str:
        """Extract soil type from query or context"""
        if context and context.get("soil_type"):
            return context["soil_type"]
        
        query_lower = query.lower()
        soil_types = ["clay", "sandy", "loam", "black", "red"]
        
        for soil in soil_types:
            if soil in query_lower:
                return soil
        
        return "loam"
    
    def _extract_weather_condition(self, query: str) -> str:
        """Extract weather condition from query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["hot", "summer", "high temperature"]):
            return "hot"
        elif any(word in query_lower for word in ["rain", "monsoon", "wet"]):
            return "rainy"
        elif any(word in query_lower for word in ["cool", "winter", "cold"]):
            return "cool"
        elif any(word in query_lower for word in ["dry", "drought", "no rain"]):
            return "dry"
        
        return "normal"
    
    def _extract_irrigation_method(self, query: str) -> str:
        """Extract irrigation method from query"""
        query_lower = query.lower()
        
        for method in self.irrigation_methods.keys():
            if method in query_lower or method.replace("_", " ") in query_lower:
                return method
        
        return "furrow"  # Default
    
    def _calculate_irrigation_plan(self, crop: str, growth_stage: str, soil_type: str, 
                                 weather_condition: str, irrigation_method: str) -> Dict:
        """Calculate irrigation plan based on parameters"""
        
        plan = {
            "crop": crop,
            "growth_stage": growth_stage,
            "irrigation_method": irrigation_method
        }
        
        if crop in self.crop_water_requirements:
            crop_data = self.crop_water_requirements[crop]
            
            # Base water requirement
            base_requirement = crop_data.get(growth_stage, 4.0)  # mm/day
            
            # Adjust for weather
            weather_factor = {
                "hot": 1.3,
                "dry": 1.4,
                "normal": 1.0,
                "cool": 0.8,
                "rainy": 0.3
            }
            
            adjusted_requirement = base_requirement * weather_factor.get(weather_condition, 1.0)
            
            # Adjust for soil type
            soil_factor = {
                "sandy": 1.2,  # More frequent irrigation needed
                "clay": 0.8,   # Retains water longer
                "loam": 1.0,
                "black": 0.9,
                "red": 1.1
            }
            
            final_requirement = adjusted_requirement * soil_factor.get(soil_type, 1.0)
            
            # Calculate irrigation frequency
            if soil_type == "sandy":
                frequency = "Daily" if final_requirement > 5 else "Every 2 days"
            elif soil_type == "clay":
                frequency = "Every 3-4 days" if final_requirement > 4 else "Weekly"
            else:
                frequency = "Every 2-3 days" if final_requirement > 4 else "Every 4-5 days"
            
            # Method efficiency
            method_data = self.irrigation_methods.get(irrigation_method, self.irrigation_methods["furrow"])
            efficiency = method_data["efficiency"]
            actual_water_needed = final_requirement / efficiency
            
            plan.update({
                "daily_requirement": round(final_requirement, 1),
                "actual_water_needed": round(actual_water_needed, 1),
                "frequency": frequency,
                "efficiency": efficiency,
                "water_saving_potential": method_data["water_saving"],
                "cost_category": method_data["cost"],
                "critical_stages": crop_data.get("critical_stages", []),
                "total_season_water": crop_data.get("total_season", 500)
            })
        else:
            # General recommendations
            plan.update({
                "daily_requirement": 4.0,
                "frequency": "Every 2-3 days",
                "efficiency": 0.6,
                "recommendation": "Consult local agricultural extension for specific crop requirements"
            })
        
        return plan
    
    def _format_irrigation_response(self, irrigation_plan: Dict, groq_response: str) -> str:
        """Format irrigation planning response"""
        
        response = "💧 **Irrigation Planning Report**\n\n"
        
        # Current requirements
        response += f"**Current Water Requirements:**\n"
        response += f"• Crop: {irrigation_plan['crop'].title()}\n"
        response += f"• Growth Stage: {irrigation_plan['growth_stage'].replace('_', ' ').title()}\n"
        response += f"• Daily Water Need: {irrigation_plan.get('daily_requirement', 'N/A')} mm/day\n"
        response += f"• Irrigation Frequency: {irrigation_plan.get('frequency', 'N/A')}\n\n"
        
        # Method efficiency
        if irrigation_plan.get("efficiency"):
            efficiency_percent = int(irrigation_plan["efficiency"] * 100)
            response += f"**Irrigation Method Analysis:**\n"
            response += f"• Method: {irrigation_plan['irrigation_method'].replace('_', ' ').title()}\n"
            response += f"• Efficiency: {efficiency_percent}%\n"
            response += f"• Water Saving Potential: {int(irrigation_plan.get('water_saving_potential', 0) * 100)}%\n"
            response += f"• Cost Category: {irrigation_plan.get('cost_category', 'Medium').title()}\n\n"
        
        # Critical stages
        if irrigation_plan.get("critical_stages"):
            response += f"**Critical Irrigation Stages:**\n"
            for stage in irrigation_plan["critical_stages"]:
                response += f"• {stage}\n"
            response += "\n"
        
        # Water conservation tips
        response += f"**Water Conservation Tips:**\n"
        response += f"• Use mulching to reduce evaporation\n"
        response += f"• Irrigate during early morning or evening\n"
        response += f"• Monitor soil moisture regularly\n"
        response += f"• Consider upgrading to efficient irrigation systems\n\n"
        
        # Detailed recommendations from Groq
        response += f"**Detailed Irrigation Plan:**\n{groq_response}\n\n"
        
        # Seasonal water budget
        if irrigation_plan.get("total_season_water"):
            total_water = irrigation_plan["total_season_water"]
            response += f"**Seasonal Water Budget:**\n"
            response += f"• Total Season Requirement: {total_water} mm\n"
            response += f"• Equivalent to: {total_water * 10} liters per square meter\n"
            response += f"• For 1 acre: ~{int(total_water * 40.47)} liters total\n"
        
        return response