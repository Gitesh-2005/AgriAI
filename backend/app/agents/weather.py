import aiohttp
import json
from typing import Dict
from datetime import datetime, timedelta
from app.agents.base import BaseAgent, AgentResponse
from app.core.config import settings

class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Weather Forecasting",
            description="Provides localized weather forecasts and agricultural insights"
        )
        self.api_key = settings.weather_api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    async def process(self, query: str, context: Dict = None) -> AgentResponse:
        """Process weather-related queries"""
        
        # Extract location from query or context
        location = self._extract_location(query, context)
        
        try:
            # Get current weather and forecast
            current_weather = await self._get_current_weather(location)
            forecast = await self._get_forecast(location)
            
            # Generate agricultural insights
            insights = self._generate_agricultural_insights(current_weather, forecast, query)
            
            response_text = self._format_weather_response(current_weather, forecast, insights)
            
            return AgentResponse(
                agent_name=self.name,
                response=response_text,
                confidence=0.9,
                metadata={
                    "location": location,
                    "current_temp": current_weather.get("main", {}).get("temp"),
                    "humidity": current_weather.get("main", {}).get("humidity"),
                    "conditions": current_weather.get("weather", [{}])[0].get("description"),
                    "forecast_days": len(forecast.get("list", [])),
                    "agricultural_alerts": insights.get("alerts", [])
                },
                citations=["OpenWeatherMap API", "IMD Weather Services"]
            )
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                response=f"Unable to fetch weather data for {location}. Please check the location name and try again.",
                confidence=0.3,
                metadata={"error": str(e), "location": location}
            )
    
    async def _get_current_weather(self, location: str) -> Dict:
        """Fetch current weather data"""
        if not self.api_key:
            return self._get_mock_weather_data()
        
        url = f"{self.base_url}/weather"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return self._get_mock_weather_data()
    
    async def _get_forecast(self, location: str) -> Dict:
        """Fetch 5-day weather forecast"""
        if not self.api_key:
            return self._get_mock_forecast_data()
        
        url = f"{self.base_url}/forecast"
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return self._get_mock_forecast_data()
    
    def _extract_location(self, query: str, context: Dict = None) -> str:
        """Extract location from query or context"""
        if context and context.get("location"):
            return context["location"]
        
        # Simple location extraction
        import re
        
        # Common Indian cities and states
        indian_locations = [
            "delhi", "mumbai", "bangalore", "chennai", "kolkata", "hyderabad",
            "pune", "ahmedabad", "jaipur", "lucknow", "kanpur", "nagpur",
            "indore", "bhopal", "ludhiana", "agra", "vadodara", "rajkot",
            "punjab", "haryana", "uttar pradesh", "bihar", "west bengal",
            "maharashtra", "karnataka", "tamil nadu", "andhra pradesh",
            "telangana", "gujarat", "rajasthan", "madhya pradesh"
        ]
        
        query_lower = query.lower()
        for location in indian_locations:
            if location in query_lower:
                return location.title()
        
        return "Delhi"  # Default location
    
    def _generate_agricultural_insights(self, current: Dict, forecast: Dict, query: str) -> Dict:
        """Generate agricultural insights from weather data"""
        insights = {
            "alerts": [],
            "recommendations": [],
            "irrigation_advice": "",
            "crop_protection": []
        }
        
        # Current conditions analysis
        temp = current.get("main", {}).get("temp", 25)
        humidity = current.get("main", {}).get("humidity", 50)
        conditions = current.get("weather", [{}])[0].get("description", "")
        
        # Temperature alerts
        if temp > 35:
            insights["alerts"].append("High temperature alert: Consider providing shade for crops")
            insights["recommendations"].append("Schedule irrigation during early morning or evening")
        elif temp < 10:
            insights["alerts"].append("Cold temperature alert: Risk of frost damage")
            insights["crop_protection"].append("Cover sensitive crops during night")
        
        # Humidity analysis
        if humidity > 80:
            insights["alerts"].append("High humidity: Increased disease risk")
            insights["crop_protection"].append("Monitor for fungal diseases")
        elif humidity < 30:
            insights["irrigation_advice"] = "Low humidity detected. Increase irrigation frequency"
        
        # Rain analysis from forecast
        rain_days = 0
        total_rainfall = 0
        
        for item in forecast.get("list", []):
            if "rain" in item:
                rain_days += 1
                total_rainfall += item["rain"].get("3h", 0)
        
        if rain_days > 0:
            insights["recommendations"].append(f"Rain expected in {rain_days} periods. Total: {total_rainfall:.1f}mm")
            if total_rainfall > 50:
                insights["irrigation_advice"] = "Heavy rain expected. Reduce irrigation and ensure proper drainage"
            else:
                insights["irrigation_advice"] = "Light to moderate rain expected. Adjust irrigation accordingly"
        else:
            insights["irrigation_advice"] = "No rain in forecast. Maintain regular irrigation schedule"
        
        return insights
    
    def _format_weather_response(self, current: Dict, forecast: Dict, insights: Dict) -> str:
        """Format weather response for agricultural context"""
        
        # Current weather
        temp = current.get("main", {}).get("temp", "N/A")
        humidity = current.get("main", {}).get("humidity", "N/A")
        conditions = current.get("weather", [{}])[0].get("description", "N/A")
        location = current.get("name", "Unknown")
        
        response = f"🌤️ **Weather Report for {location}**\n\n"
        response += f"**Current Conditions:**\n"
        response += f"• Temperature: {temp}°C\n"
        response += f"• Humidity: {humidity}%\n"
        response += f"• Conditions: {conditions.title()}\n\n"
        
        # 5-day forecast summary
        if forecast.get("list"):
            response += f"**5-Day Forecast:**\n"
            daily_data = {}
            
            for item in forecast["list"][:8]:  # Next 24 hours (8 x 3-hour intervals)
                date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
                if date not in daily_data:
                    daily_data[date] = {
                        "temp_min": item["main"]["temp"],
                        "temp_max": item["main"]["temp"],
                        "conditions": item["weather"][0]["description"],
                        "rain": item.get("rain", {}).get("3h", 0)
                    }
                else:
                    daily_data[date]["temp_min"] = min(daily_data[date]["temp_min"], item["main"]["temp"])
                    daily_data[date]["temp_max"] = max(daily_data[date]["temp_max"], item["main"]["temp"])
                    daily_data[date]["rain"] += item.get("rain", {}).get("3h", 0)
            
            for date, data in list(daily_data.items())[:3]:
                formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %B %d")
                response += f"• {formatted_date}: {data['temp_min']:.0f}-{data['temp_max']:.0f}°C, {data['conditions']}"
                if data['rain'] > 0:
                    response += f", Rain: {data['rain']:.1f}mm"
                response += "\n"
        
        # Agricultural insights
        response += f"\n🌾 **Agricultural Insights:**\n"
        
        if insights["alerts"]:
            response += f"**⚠️ Alerts:**\n"
            for alert in insights["alerts"]:
                response += f"• {alert}\n"
            response += "\n"
        
        if insights["irrigation_advice"]:
            response += f"**💧 Irrigation Advice:**\n• {insights['irrigation_advice']}\n\n"
        
        if insights["recommendations"]:
            response += f"**📋 Recommendations:**\n"
            for rec in insights["recommendations"]:
                response += f"• {rec}\n"
        
        if insights["crop_protection"]:
            response += f"**🛡️ Crop Protection:**\n"
            for protection in insights["crop_protection"]:
                response += f"• {protection}\n"
        
        return response
    
    def _get_mock_weather_data(self) -> Dict:
        """Mock weather data for development"""
        return {
            "name": "Delhi",
            "main": {
                "temp": 28.5,
                "humidity": 65,
                "pressure": 1012
            },
            "weather": [
                {
                    "description": "partly cloudy",
                    "main": "Clouds"
                }
            ]
        }
    
    def _get_mock_forecast_data(self) -> Dict:
        """Mock forecast data for development"""
        return {
            "list": [
                {
                    "dt": int(datetime.now().timestamp()) + (i * 10800),  # 3-hour intervals
                    "main": {
                        "temp": 28 + (i % 3) - 1,
                        "humidity": 60 + (i % 4) * 5
                    },
                    "weather": [{"description": "clear sky" if i % 2 == 0 else "light rain"}],
                    "rain": {"3h": 2.5} if i % 3 == 0 else {}
                }
                for i in range(8)
            ]
        }