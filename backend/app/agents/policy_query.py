import json
from typing import Dict, List
from app.agents.base import BaseAgent, AgentResponse
from app.services.groq_service import GroqService

class PolicyQueryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Policy & Regulations",
            description="Provides information on agricultural policies, laws, and regulations"
        )
        self.groq_service = GroqService()
        
        # Major agricultural policies and acts
        self.policies = {
            "msp": {
                "name": "Minimum Support Price",
                "description": "Government announced minimum price for agricultural commodities",
                "crops_covered": ["Rice", "Wheat", "Cotton", "Sugarcane", "Pulses", "Oilseeds"],
                "announcement": "Before sowing season",
                "procurement_agencies": ["FCI", "NAFED", "CCI"]
            },
            "apmc": {
                "name": "Agricultural Produce Market Committee",
                "description": "Regulates agricultural markets and trading",
                "key_points": ["Market regulation", "License requirements", "Fee structure"],
                "recent_reforms": ["eNAM integration", "Direct marketing", "Private markets"]
            },
            "contract_farming": {
                "name": "Contract Farming Act 2020",
                "description": "Framework for contract farming agreements",
                "benefits": ["Assured market", "Price certainty", "Technology transfer"],
                "protections": ["No land ownership transfer", "Dispute resolution"]
            },
            "land_reforms": {
                "name": "Land Reforms",
                "description": "State-specific land ownership and transfer laws",
                "key_aspects": ["Land ceiling", "Tenancy rights", "Land records"],
                "digitization": ["Land records digitization", "Online mutation"]
            },
            "water_rights": {
                "name": "Water Rights and Irrigation",
                "description": "Water allocation and irrigation policies",
                "key_points": ["Water sharing", "Groundwater regulation", "Irrigation subsidies"],
                "conservation": ["Drip irrigation subsidy", "Water harvesting"]
            }
        }
        
        # Government schemes and their policy framework
        self.scheme_policies = {
            "pm_kisan": {
                "policy_framework": "Direct Benefit Transfer",
                "eligibility_criteria": "Land ownership based",
                "exclusions": ["Income tax payers", "Government employees"],
                "implementation": "State government verification"
            },
            "fasal_bima": {
                "policy_framework": "Risk mitigation through insurance",
                "coverage": "Weather and non-weather risks",
                "premium_sharing": "Government subsidized",
                "claim_settlement": "Technology-based assessment"
            },
            "soil_health": {
                "policy_framework": "Sustainable agriculture promotion",
                "testing_frequency": "Every 3 years",
                "recommendations": "Crop and soil specific",
                "implementation": "Through soil testing labs"
            }
        }
        
        # State-specific policies (sample)
        self.state_policies = {
            "punjab": {
                "crop_diversification": "Incentives for non-paddy crops",
                "stubble_burning": "Penalties and alternatives",
                "water_conservation": "Drip irrigation subsidies"
            },
            "maharashtra": {
                "drought_management": "Drought-proofing programs",
                "horticulture_promotion": "Fruit and vegetable subsidies",
                "organic_farming": "Certification support"
            },
            "karnataka": {
                "watershed_development": "Rainwater harvesting",
                "precision_farming": "Technology adoption support",
                "farmer_producer_organizations": "FPO promotion"
            }
        }
    
    async def process(self, query: str, context: Dict = None) -> AgentResponse:
        """Process policy and regulation queries"""
        
        # Classify policy query type
        policy_type = self._classify_policy_query(query)
        location = self._extract_location(query, context)
        
        # Generate policy information
        policy_info = self._get_policy_information(policy_type, location, query)
        
        # Use Groq for detailed policy explanation
        groq_prompt = f"""
        As a policy expert in Indian agriculture, provide comprehensive information about:
        
        Query: {query}
        Policy Type: {policy_type}
        Location: {location}
        
        Provide detailed explanation covering:
        1. Policy objectives and scope
        2. Implementation mechanism
        3. Eligibility criteria and procedures
        4. Benefits and limitations
        5. Recent updates or amendments
        6. Practical implications for farmers
        
        Include specific steps for compliance or application where relevant.
        """
        
        groq_response = await self.groq_service.generate_response(groq_prompt)
        
        # Format comprehensive response
        response_text = self._format_policy_response(policy_info, groq_response, policy_type)
        
        return AgentResponse(
            agent_name=self.name,
            response=response_text,
            confidence=0.85,
            metadata={
                "policy_type": policy_type,
                "location": location,
                "applicable_schemes": policy_info.get("applicable_schemes", []),
                "compliance_required": policy_info.get("compliance_required", False)
            },
            citations=["Ministry of Agriculture & FW", "State Agriculture Departments", "Agricultural Acts & Policies"]
        )
    
    def _classify_policy_query(self, query: str) -> str:
        """Classify the type of policy query"""
        query_lower = query.lower()
        
        policy_keywords = {
            "msp": ["msp", "minimum support price", "procurement", "government price"],
            "apmc": ["apmc", "mandi", "market committee", "agricultural market"],
            "contract_farming": ["contract farming", "agreement", "contract", "buyer"],
            "land_reforms": ["land", "ownership", "records", "mutation", "title"],
            "water_rights": ["water", "irrigation", "groundwater", "water rights"],
            "subsidy": ["subsidy", "scheme", "benefit", "support", "assistance"],
            "tax": ["tax", "income tax", "agricultural income", "exemption"],
            "export_import": ["export", "import", "trade", "international"],
            "organic": ["organic", "certification", "natural farming"],
            "labor": ["labor", "workers", "employment", "wages"]
        }
        
        for policy_type, keywords in policy_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return policy_type
        
        return "general"
    
    def _extract_location(self, query: str, context: Dict = None) -> str:
        """Extract location for state-specific policies"""
        if context and context.get("location"):
            return context["location"].lower()
        
        query_lower = query.lower()
        states = ["punjab", "haryana", "maharashtra", "karnataka", "tamil nadu", 
                 "andhra pradesh", "telangana", "gujarat", "rajasthan", "madhya pradesh"]
        
        for state in states:
            if state in query_lower:
                return state
        
        return "general"
    
    def _get_policy_information(self, policy_type: str, location: str, query: str) -> Dict:
        """Get relevant policy information"""
        info = {
            "policy_type": policy_type,
            "location": location,
            "applicable_schemes": [],
            "compliance_required": False
        }
        
        # Get central policy information
        if policy_type in self.policies:
            info["central_policy"] = self.policies[policy_type]
        
        # Get scheme-specific policy information
        if policy_type in self.scheme_policies:
            info["scheme_policy"] = self.scheme_policies[policy_type]
            info["applicable_schemes"].append(policy_type)
        
        # Get state-specific information
        if location != "general" and location in self.state_policies:
            info["state_policy"] = self.state_policies[location]
        
        # Determine if compliance is required
        compliance_keywords = ["license", "registration", "permit", "approval", "compliance"]
        if any(keyword in query.lower() for keyword in compliance_keywords):
            info["compliance_required"] = True
        
        return info
    
    def _format_policy_response(self, policy_info: Dict, groq_response: str, policy_type: str) -> str:
        """Format comprehensive policy response"""
        
        response = "🏛️ **Agricultural Policy Information**\n\n"
        
        # Central policy information
        if "central_policy" in policy_info:
            central = policy_info["central_policy"]
            response += f"**{central['name']}**\n"
            response += f"• Description: {central['description']}\n"
            
            if "crops_covered" in central:
                response += f"• Crops Covered: {', '.join(central['crops_covered'])}\n"
            if "key_points" in central:
                response += f"• Key Points: {', '.join(central['key_points'])}\n"
            if "benefits" in central:
                response += f"• Benefits: {', '.join(central['benefits'])}\n"
            
            response += "\n"
        
        # Scheme-specific policy
        if "scheme_policy" in policy_info:
            scheme = policy_info["scheme_policy"]
            response += f"**Policy Framework:**\n"
            response += f"• Framework: {scheme['policy_framework']}\n"
            
            if "eligibility_criteria" in scheme:
                response += f"• Eligibility: {scheme['eligibility_criteria']}\n"
            if "implementation" in scheme:
                response += f"• Implementation: {scheme['implementation']}\n"
            
            response += "\n"
        
        # State-specific policies
        if "state_policy" in policy_info:
            state_name = policy_info["location"].title()
            response += f"**{state_name} State Policies:**\n"
            for key, value in policy_info["state_policy"].items():
                response += f"• {key.replace('_', ' ').title()}: {value}\n"
            response += "\n"
        
        # Compliance requirements
        if policy_info.get("compliance_required"):
            response += f"**Compliance Requirements:**\n"
            response += f"• Check with local authorities for specific requirements\n"
            response += f"• Ensure all documentation is complete\n"
            response += f"• Follow prescribed procedures and timelines\n"
            response += f"• Maintain records for future reference\n\n"
        
        # Detailed explanation from Groq
        response += f"**Detailed Policy Analysis:**\n{groq_response}\n\n"
        
        # Important contacts and resources
        response += f"**Important Resources:**\n"
        response += f"• Ministry of Agriculture: agricoop.gov.in\n"
        response += f"• State Agriculture Department\n"
        response += f"• District Collector Office\n"
        response += f"• Agricultural Extension Officer\n"
        response += f"• Common Service Centers (CSC)\n\n"
        
        # Recent updates note
        response += f"**📝 Note:** Policy information is subject to updates. Please verify current status from official sources before taking any action."
        
        return response