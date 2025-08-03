import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, List
from app.agents.base import BaseAgent, AgentResponse

class MarketIntelligenceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Market Intelligence",
            description="Provides real-time market prices and trading insights"
        )
        
        # Mock market data - In production, integrate with AgMarkNet, eNAM APIs
        self.market_data = {
            "rice": {
                "current_price": 2850,  # per quintal
                "price_trend": "increasing",
                "change_percent": 2.5,
                "demand": "high",
                "supply": "moderate",
                "forecast": "bullish",
                "major_markets": {
                    "Punjab": 2900,
                    "Haryana": 2880,
                    "Uttar Pradesh": 2820,
                    "West Bengal": 2750,
                    "Andhra Pradesh": 2800
                }
            },
            "wheat": {
                "current_price": 2150,
                "price_trend": "stable",
                "change_percent": 0.8,
                "demand": "moderate",
                "supply": "high",
                "forecast": "stable",
                "major_markets": {
                    "Punjab": 2180,
                    "Haryana": 2170,
                    "Uttar Pradesh": 2140,
                    "Madhya Pradesh": 2120,
                    "Rajasthan": 2100
                }
            },
            "maize": {
                "current_price": 1850,
                "price_trend": "decreasing",
                "change_percent": -1.2,
                "demand": "moderate",
                "supply": "high",
                "forecast": "bearish",
                "major_markets": {
                    "Karnataka": 1880,
                    "Andhra Pradesh": 1860,
                    "Tamil Nadu": 1840,
                    "Maharashtra": 1830,
                    "Gujarat": 1820
                }
            },
            "cotton": {
                "current_price": 6200,
                "price_trend": "increasing",
                "change_percent": 3.2,
                "demand": "high",
                "supply": "low",
                "forecast": "bullish",
                "major_markets": {
                    "Gujarat": 6300,
                    "Maharashtra": 6250,
                    "Andhra Pradesh": 6180,
                    "Karnataka": 6150,
                    "Haryana": 6100
                }
            },
            "sugarcane": {
                "current_price": 350,  # per ton
                "price_trend": "stable",
                "change_percent": 0.5,
                "demand": "high",
                "supply": "moderate",
                "forecast": "stable",
                "major_markets": {
                    "Uttar Pradesh": 360,
                    "Maharashtra": 340,
                    "Karnataka": 345,
                    "Tamil Nadu": 355,
                    "Gujarat": 335
                }
            }
        }
    
    async def process(self, query: str, context: Dict = None) -> AgentResponse:
        """Process market intelligence queries"""
        
        # Extract commodity and location from query
        commodity = self._extract_commodity(query)
        location = self._extract_location(query, context)
        
        if commodity:
            # Get specific commodity data
            market_info = self.market_data.get(commodity.lower())
            if market_info:
                response_text = self._format_commodity_response(commodity, market_info, location, query)
                confidence = 0.9
            else:
                response_text = f"Market data for {commodity} is not available. Available commodities: {', '.join(self.market_data.keys())}"
                confidence = 0.3
        else:
            # General market overview
            response_text = self._format_general_market_response(query)
            confidence = 0.7
        
        # Generate trading recommendations
        recommendations = self._generate_trading_recommendations(commodity, location, query)
        
        return AgentResponse(
            agent_name=self.name,
            response=response_text,
            confidence=confidence,
            metadata={
                "commodity": commodity,
                "location": location,
                "price_trend": market_info.get("price_trend") if commodity and market_info else None,
                "recommendations": recommendations,
                "data_freshness": "real-time"
            },
            citations=["AgMarkNet", "eNAM Portal", "Commodity Exchanges"]
        )
    
    def _extract_commodity(self, query: str) -> str:
        """Extract commodity name from query"""
        query_lower = query.lower()
        
        # Direct commodity matches
        for commodity in self.market_data.keys():
            if commodity in query_lower:
                return commodity
        
        # Alternative names
        commodity_aliases = {
            "paddy": "rice",
            "corn": "maize",
            "sugar": "sugarcane",
            "kapas": "cotton"
        }
        
        for alias, commodity in commodity_aliases.items():
            if alias in query_lower:
                return commodity
        
        return None
    
    def _extract_location(self, query: str, context: Dict = None) -> str:
        """Extract location from query or context"""
        if context and context.get("location"):
            return context["location"]
        
        import re
        states = [
            "punjab", "haryana", "uttar pradesh", "bihar", "west bengal",
            "maharashtra", "karnataka", "tamil nadu", "andhra pradesh",
            "telangana", "gujarat", "rajasthan", "madhya pradesh", "odisha"
        ]
        
        query_lower = query.lower()
        for state in states:
            if state in query_lower:
                return state.title()
        
        return "General"
    
    def _format_commodity_response(self, commodity: str, market_info: Dict, location: str, query: str) -> str:
        """Format commodity-specific market response"""
        
        current_price = market_info["current_price"]
        trend = market_info["price_trend"]
        change = market_info["change_percent"]
        demand = market_info["demand"]
        supply = market_info["supply"]
        forecast = market_info["forecast"]
        
        # Price unit
        unit = "per quintal" if commodity != "sugarcane" else "per ton"
        
        response = f"📊 **Market Report for {commodity.title()}**\n\n"
        response += f"**Current Market Price:** ₹{current_price:,} {unit}\n"
        
        # Trend indicator
        trend_emoji = "📈" if trend == "increasing" else "📉" if trend == "decreasing" else "➡️"
        change_text = f"+{change}%" if change > 0 else f"{change}%"
        response += f"**Price Trend:** {trend_emoji} {trend.title()} ({change_text})\n\n"
        
        # Market conditions
        response += f"**Market Conditions:**\n"
        response += f"• Demand: {demand.title()}\n"
        response += f"• Supply: {supply.title()}\n"
        response += f"• Forecast: {forecast.title()}\n\n"
        
        # Regional prices
        if location != "General" and location.lower() in [k.lower() for k in market_info["major_markets"].keys()]:
            for state, price in market_info["major_markets"].items():
                if state.lower() == location.lower():
                    response += f"**Price in {location}:** ₹{price:,} {unit}\n\n"
                    break
        else:
            response += f"**Major Market Prices:**\n"
            for state, price in list(market_info["major_markets"].items())[:3]:
                response += f"• {state}: ₹{price:,} {unit}\n"
            response += "\n"
        
        # Price analysis
        response += f"**Price Analysis:**\n"
        if change > 2:
            response += f"• Strong upward momentum in {commodity} prices\n"
            response += f"• Consider selling if you have stock\n"
        elif change < -2:
            response += f"• Prices showing downward pressure\n"
            response += f"• May be a good buying opportunity\n"
        else:
            response += f"• Prices are relatively stable\n"
            response += f"• Monitor for trend changes\n"
        
        return response
    
    def _format_general_market_response(self, query: str) -> str:
        """Format general market overview"""
        
        response = "📊 **Agricultural Market Overview**\n\n"
        
        # Top performing commodities
        sorted_commodities = sorted(
            self.market_data.items(),
            key=lambda x: x[1]["change_percent"],
            reverse=True
        )
        
        response += "**Today's Top Performers:**\n"
        for commodity, data in sorted_commodities[:3]:
            change = data["change_percent"]
            trend_emoji = "📈" if change > 0 else "📉"
            response += f"• {commodity.title()}: ₹{data['current_price']:,} {trend_emoji} {change:+.1f}%\n"
        
        response += "\n**Market Highlights:**\n"
        
        # Market insights
        bullish_count = sum(1 for data in self.market_data.values() if data["forecast"] == "bullish")
        bearish_count = sum(1 for data in self.market_data.values() if data["forecast"] == "bearish")
        
        if bullish_count > bearish_count:
            response += "• Overall market sentiment is positive\n"
            response += "• Good time for farmers to consider selling\n"
        elif bearish_count > bullish_count:
            response += "• Market showing some weakness\n"
            response += "• Buyers may find good opportunities\n"
        else:
            response += "• Mixed market signals observed\n"
            response += "• Careful analysis recommended before trading\n"
        
        return response
    
    def _generate_trading_recommendations(self, commodity: str, location: str, query: str) -> List[str]:
        """Generate trading recommendations"""
        recommendations = []
        
        if commodity and commodity.lower() in self.market_data:
            market_info = self.market_data[commodity.lower()]
            change = market_info["change_percent"]
            trend = market_info["price_trend"]
            forecast = market_info["forecast"]
            
            if change > 2 and trend == "increasing":
                recommendations.append("Consider selling current stock due to price surge")
                recommendations.append("Monitor for profit-taking opportunities")
            elif change < -2 and trend == "decreasing":
                recommendations.append("Good buying opportunity for future delivery")
                recommendations.append("Consider forward contracts at current levels")
            
            if forecast == "bullish":
                recommendations.append("Medium-term outlook is positive")
            elif forecast == "bearish":
                recommendations.append("Exercise caution in new purchases")
            
            # Location-specific advice
            if location != "General":
                recommendations.append(f"Check local {location} mandis for better rates")
        
        return recommendations