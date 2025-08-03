import json
from typing import Dict, List
from app.agents.base import BaseAgent, AgentResponse
from app.services.groq_service import GroqService

class FinancialPlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Financial Planning",
            description="Provides financial planning, loan guidance, and profitability analysis for farmers"
        )
        self.groq_service = GroqService()
        
        # Crop economics data (per acre in INR)
        self.crop_economics = {
            "rice": {
                "input_cost": 25000,
                "expected_yield": 25,  # quintals
                "market_price": 2800,  # per quintal
                "gross_income": 70000,
                "net_profit": 45000,
                "break_even_price": 1000,
                "risk_level": "medium"
            },
            "wheat": {
                "input_cost": 20000,
                "expected_yield": 20,
                "market_price": 2150,
                "gross_income": 43000,
                "net_profit": 23000,
                "break_even_price": 1000,
                "risk_level": "low"
            },
            "cotton": {
                "input_cost": 35000,
                "expected_yield": 8,
                "market_price": 6200,
                "gross_income": 49600,
                "net_profit": 14600,
                "break_even_price": 4375,
                "risk_level": "high"
            },
            "sugarcane": {
                "input_cost": 45000,
                "expected_yield": 400,  # quintals
                "market_price": 350,
                "gross_income": 140000,
                "net_profit": 95000,
                "break_even_price": 112,
                "risk_level": "medium"
            }
        }
        
        # Government schemes and subsidies
        self.schemes = {
            "pm_kisan": {
                "name": "PM-KISAN",
                "amount": 6000,
                "frequency": "annual",
                "eligibility": "All farmers with cultivable land",
                "documents": ["Aadhaar", "Land records", "Bank account"]
            },
            "crop_insurance": {
                "name": "Pradhan Mantri Fasal Bima Yojana",
                "premium": "2% for Kharif, 1.5% for Rabi",
                "coverage": "Up to sum insured",
                "eligibility": "All farmers",
                "documents": ["Land records", "Sowing certificate", "Bank account"]
            },
            "kcc": {
                "name": "Kisan Credit Card",
                "interest_rate": "7% (with subsidy: 4%)",
                "limit": "Based on land holding and crop",
                "eligibility": "Farmers with land records",
                "documents": ["Land records", "Identity proof", "Address proof"]
            },
            "soil_health_card": {
                "name": "Soil Health Card Scheme",
                "subsidy": "Free soil testing",
                "frequency": "Every 3 years",
                "eligibility": "All farmers",
                "documents": ["Land records"]
            }
        }
        
        # Loan products
        self.loan_products = {
            "crop_loan": {
                "purpose": "Seasonal agricultural operations",
                "interest_rate": "7-9%",
                "tenure": "Up to 12 months",
                "amount": "Based on scale of finance",
                "collateral": "Hypothecation of crops"
            },
            "term_loan": {
                "purpose": "Farm development, equipment",
                "interest_rate": "8-12%",
                "tenure": "3-7 years",
                "amount": "Up to Rs. 50 lakhs",
                "collateral": "Land/equipment mortgage"
            },
            "self_help_group": {
                "purpose": "Small scale farming activities",
                "interest_rate": "6-8%",
                "tenure": "1-3 years",
                "amount": "Up to Rs. 10 lakhs per group",
                "collateral": "Group guarantee"
            }
        }
    
    async def process(self, query: str, context: Dict = None) -> AgentResponse:
        """Process financial planning queries"""
        
        # Determine query type
        query_type = self._classify_financial_query(query)
        
        if query_type == "profitability":
            response_data = await self._handle_profitability_query(query, context)
        elif query_type == "loan":
            response_data = await self._handle_loan_query(query, context)
        elif query_type == "subsidy":
            response_data = await self._handle_subsidy_query(query, context)
        elif query_type == "insurance":
            response_data = await self._handle_insurance_query(query, context)
        else:
            response_data = await self._handle_general_financial_query(query, context)
        
        return AgentResponse(
            agent_name=self.name,
            response=response_data["response"],
            confidence=response_data["confidence"],
            metadata=response_data["metadata"],
            citations=["Ministry of Agriculture", "NABARD", "Banking Regulations", "Government Schemes"]
        )
    
    def _classify_financial_query(self, query: str) -> str:
        """Classify the type of financial query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["profit", "cost", "income", "budget", "economics"]):
            return "profitability"
        elif any(word in query_lower for word in ["loan", "credit", "kcc", "borrow", "finance"]):
            return "loan"
        elif any(word in query_lower for word in ["subsidy", "scheme", "pm-kisan", "government support"]):
            return "subsidy"
        elif any(word in query_lower for word in ["insurance", "fasal bima", "crop insurance"]):
            return "insurance"
        else:
            return "general"
    
    async def _handle_profitability_query(self, query: str, context: Dict = None) -> Dict:
        """Handle profitability and cost analysis queries"""
        
        crop = self._extract_crop(query, context)
        area = self._extract_area(query, context)
        
        if crop in self.crop_economics:
            crop_data = self.crop_economics[crop]
            
            # Calculate for specified area
            total_input_cost = crop_data["input_cost"] * area
            total_gross_income = crop_data["gross_income"] * area
            total_net_profit = crop_data["net_profit"] * area
            
            # Use Groq for detailed financial analysis
            groq_prompt = f"""
            As a financial advisor for farmers, provide detailed cost-benefit analysis for:
            
            Crop: {crop}
            Area: {area} acres
            Input Cost: Rs. {total_input_cost:,}
            Expected Income: Rs. {total_gross_income:,}
            Net Profit: Rs. {total_net_profit:,}
            
            Provide analysis on:
            1. Detailed cost breakdown
            2. Revenue optimization strategies
            3. Risk mitigation measures
            4. Alternative crop suggestions
            5. Financial planning recommendations
            6. Break-even analysis
            
            Include practical tips for cost reduction and income enhancement.
            """
            
            groq_response = await self.groq_service.generate_response(groq_prompt)
            
            response_text = f"💰 **Profitability Analysis for {crop.title()}**\n\n"
            response_text += f"**Area:** {area} acre(s)\n\n"
            response_text += f"**Financial Projections:**\n"
            response_text += f"• Total Input Cost: ₹{total_input_cost:,}\n"
            response_text += f"• Expected Gross Income: ₹{total_gross_income:,}\n"
            response_text += f"• Projected Net Profit: ₹{total_net_profit:,}\n"
            response_text += f"• Profit Margin: {int((total_net_profit/total_gross_income)*100)}%\n"
            response_text += f"• Break-even Price: ₹{crop_data['break_even_price']}/quintal\n"
            response_text += f"• Risk Level: {crop_data['risk_level'].title()}\n\n"
            response_text += f"**Detailed Analysis:**\n{groq_response}"
            
            return {
                "response": response_text,
                "confidence": 0.9,
                "metadata": {
                    "crop": crop,
                    "area": area,
                    "total_investment": total_input_cost,
                    "expected_profit": total_net_profit,
                    "risk_level": crop_data["risk_level"]
                }
            }
        else:
            return {
                "response": f"Detailed profitability data for {crop} is not available. Please consult local agricultural extension officer for crop-specific economics.",
                "confidence": 0.4,
                "metadata": {"crop": crop, "data_available": False}
            }
    
    async def _handle_loan_query(self, query: str, context: Dict = None) -> Dict:
        """Handle loan and credit queries"""
        
        loan_type = self._extract_loan_type(query)
        amount = self._extract_amount(query)
        
        response_text = "🏦 **Agricultural Loan Information**\n\n"
        
        if loan_type in self.loan_products:
            loan_info = self.loan_products[loan_type]
            response_text += f"**{loan_info['purpose']}**\n"
            response_text += f"• Interest Rate: {loan_info['interest_rate']}\n"
            response_text += f"• Tenure: {loan_info['tenure']}\n"
            response_text += f"• Maximum Amount: {loan_info['amount']}\n"
            response_text += f"• Collateral: {loan_info['collateral']}\n\n"
        
        # Add general loan guidance
        response_text += f"**Available Loan Products:**\n"
        for loan_name, loan_data in self.loan_products.items():
            response_text += f"• **{loan_name.replace('_', ' ').title()}**: {loan_data['purpose']}\n"
        
        response_text += f"\n**Required Documents:**\n"
        response_text += f"• Land ownership documents\n"
        response_text += f"• Identity and address proof\n"
        response_text += f"• Income proof/crop details\n"
        response_text += f"• Bank statements\n"
        response_text += f"• Passport size photographs\n\n"
        
        if amount:
            # Calculate EMI for term loan
            monthly_rate = 0.10 / 12  # Assuming 10% annual rate
            tenure_months = 60  # 5 years
            emi = (amount * monthly_rate * (1 + monthly_rate)**tenure_months) / ((1 + monthly_rate)**tenure_months - 1)
            response_text += f"**EMI Calculation (for ₹{amount:,} at 10% for 5 years):**\n"
            response_text += f"• Monthly EMI: ₹{int(emi):,}\n"
            response_text += f"• Total Interest: ₹{int(emi * tenure_months - amount):,}\n\n"
        
        response_text += f"**Application Process:**\n"
        response_text += f"1. Visit nearest bank branch or CSC center\n"
        response_text += f"2. Fill loan application form\n"
        response_text += f"3. Submit required documents\n"
        response_text += f"4. Bank verification and assessment\n"
        response_text += f"5. Loan approval and disbursement\n"
        
        return {
            "response": response_text,
            "confidence": 0.85,
            "metadata": {
                "loan_type": loan_type,
                "amount_requested": amount,
                "emi_calculated": amount is not None
            }
        }
    
    async def _handle_subsidy_query(self, query: str, context: Dict = None) -> Dict:
        """Handle subsidy and government scheme queries"""
        
        response_text = "🏛️ **Government Schemes & Subsidies**\n\n"
        
        # Check for specific scheme mention
        scheme_mentioned = None
        query_lower = query.lower()
        for scheme_key, scheme_data in self.schemes.items():
            if scheme_key.replace("_", " ") in query_lower or scheme_data["name"].lower() in query_lower:
                scheme_mentioned = scheme_key
                break
        
        if scheme_mentioned:
            scheme = self.schemes[scheme_mentioned]
            response_text += f"**{scheme['name']}**\n"
            if "amount" in scheme:
                response_text += f"• Benefit: ₹{scheme['amount']:,} {scheme.get('frequency', '')}\n"
            if "premium" in scheme:
                response_text += f"• Premium: {scheme['premium']}\n"
            if "coverage" in scheme:
                response_text += f"• Coverage: {scheme['coverage']}\n"
            response_text += f"• Eligibility: {scheme['eligibility']}\n"
            response_text += f"• Required Documents: {', '.join(scheme['documents'])}\n\n"
        
        # List all major schemes
        response_text += f"**Major Agricultural Schemes:**\n\n"
        for scheme_key, scheme_data in self.schemes.items():
            response_text += f"**{scheme_data['name']}**\n"
            if "amount" in scheme_data:
                response_text += f"• Benefit: ₹{scheme_data['amount']:,} {scheme_data.get('frequency', '')}\n"
            response_text += f"• Eligibility: {scheme_data['eligibility']}\n\n"
        
        response_text += f"**How to Apply:**\n"
        response_text += f"1. Visit Common Service Center (CSC) or online portal\n"
        response_text += f"2. Register with Aadhaar and mobile number\n"
        response_text += f"3. Fill application form with required details\n"
        response_text += f"4. Upload necessary documents\n"
        response_text += f"5. Submit application and track status\n\n"
        
        response_text += f"**Important Portals:**\n"
        response_text += f"• PM-KISAN: pmkisan.gov.in\n"
        response_text += f"• Crop Insurance: pmfby.gov.in\n"
        response_text += f"• DBT Agriculture: dbtbharat.gov.in\n"
        
        return {
            "response": response_text,
            "confidence": 0.9,
            "metadata": {
                "scheme_mentioned": scheme_mentioned,
                "total_schemes": len(self.schemes)
            }
        }
    
    async def _handle_insurance_query(self, query: str, context: Dict = None) -> Dict:
        """Handle crop insurance queries"""
        
        crop = self._extract_crop(query, context)
        area = self._extract_area(query, context)
        
        response_text = "🛡️ **Crop Insurance Information**\n\n"
        response_text += f"**Pradhan Mantri Fasal Bima Yojana (PMFBY)**\n\n"
        
        # Premium calculation
        if crop and area:
            # Estimate sum insured (based on average)
            sum_insured_per_acre = 40000  # Average sum insured
            total_sum_insured = sum_insured_per_acre * area
            
            # Premium rates
            kharif_premium = total_sum_insured * 0.02  # 2% for Kharif
            rabi_premium = total_sum_insured * 0.015   # 1.5% for Rabi
            
            response_text += f"**For {crop.title()} - {area} acre(s):**\n"
            response_text += f"• Estimated Sum Insured: ₹{total_sum_insured:,}\n"
            response_text += f"• Kharif Premium: ₹{int(kharif_premium):,} (2%)\n"
            response_text += f"• Rabi Premium: ₹{int(rabi_premium):,} (1.5%)\n\n"
        
        response_text += f"**Coverage Details:**\n"
        response_text += f"• Pre-sowing losses (prevented sowing)\n"
        response_text += f"• Standing crop losses (drought, flood, pest)\n"
        response_text += f"• Post-harvest losses (cyclone, rainfall)\n"
        response_text += f"• Localized calamities (hailstorm, landslide)\n\n"
        
        response_text += f"**Premium Rates:**\n"
        response_text += f"• Kharif crops: 2% of sum insured\n"
        response_text += f"• Rabi crops: 1.5% of sum insured\n"
        response_text += f"• Annual commercial/horticultural: 5%\n\n"
        
        response_text += f"**How to Apply:**\n"
        response_text += f"1. Visit bank branch or CSC center\n"
        response_text += f"2. Fill insurance application form\n"
        response_text += f"3. Submit land records and identity proof\n"
        response_text += f"4. Pay premium amount\n"
        response_text += f"5. Get insurance certificate\n\n"
        
        response_text += f"**Important Dates:**\n"
        response_text += f"• Kharif: Apply by July 31st\n"
        response_text += f"• Rabi: Apply by December 31st\n"
        response_text += f"• Late applications may be accepted with penalty\n"
        
        return {
            "response": response_text,
            "confidence": 0.88,
            "metadata": {
                "crop": crop,
                "area": area,
                "insurance_type": "PMFBY"
            }
        }
    
    async def _handle_general_financial_query(self, query: str, context: Dict = None) -> Dict:
        """Handle general financial queries"""
        
        groq_prompt = f"""
        As a financial advisor specializing in agriculture, provide comprehensive guidance for:
        
        Query: {query}
        Context: {json.dumps(context) if context else "General farming context"}
        
        Provide practical advice on:
        1. Financial planning for farmers
        2. Investment strategies in agriculture
        3. Risk management techniques
        4. Government support utilization
        5. Income diversification options
        
        Include specific actionable recommendations.
        """
        
        groq_response = await self.groq_service.generate_response(groq_prompt)
        
        response_text = "💼 **Financial Planning Guidance**\n\n"
        response_text += groq_response
        
        return {
            "response": response_text,
            "confidence": 0.75,
            "metadata": {"query_type": "general_financial"}
        }
    
    def _extract_crop(self, query: str, context: Dict = None) -> str:
        """Extract crop from query or context"""
        if context and context.get("crop_type"):
            return context["crop_type"]
        
        query_lower = query.lower()
        for crop in self.crop_economics.keys():
            if crop in query_lower:
                return crop
        
        return "general"
    
    def _extract_area(self, query: str, context: Dict = None) -> float:
        """Extract area from query or context"""
        if context and context.get("farm_size"):
            try:
                return float(context["farm_size"])
            except:
                pass
        
        import re
        area_match = re.search(r'(\d+\.?\d*)\s*(acre|hectare)', query.lower())
        if area_match:
            area = float(area_match.group(1))
            unit = area_match.group(2)
            if unit == "hectare":
                area = area * 2.47  # Convert to acres
            return area
        
        return 1.0  # Default 1 acre
    
    def _extract_loan_type(self, query: str) -> str:
        """Extract loan type from query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["kcc", "credit card", "kisan credit"]):
            return "crop_loan"
        elif any(word in query_lower for word in ["term", "equipment", "machinery", "development"]):
            return "term_loan"
        elif any(word in query_lower for word in ["shg", "self help", "group"]):
            return "self_help_group"
        
        return "crop_loan"  # Default
    
    def _extract_amount(self, query: str) -> int:
        """Extract loan amount from query"""
        import re
        
        # Look for amount patterns
        amount_patterns = [
            r'(\d+)\s*lakh',
            r'(\d+)\s*crore',
            r'rs\.?\s*(\d+)',
            r'rupees\s*(\d+)',
            r'₹\s*(\d+)'
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, query.lower())
            if match:
                amount = int(match.group(1))
                if 'lakh' in pattern:
                    return amount * 100000
                elif 'crore' in pattern:
                    return amount * 10000000
                else:
                    return amount
        
        return None