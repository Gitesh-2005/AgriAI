import json
from typing import Dict, List
from app.agents.base import BaseAgent, AgentResponse
from app.services.groq_service import GroqService

class PestDiseaseAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Pest & Disease Management",
            description="Diagnoses crop diseases and pest problems with treatment recommendations"
        )
        self.groq_service = GroqService()
        
        # Common pest and disease database
        self.pest_disease_db = {
            "rice": {
                "pests": {
                    "brown_planthopper": {
                        "symptoms": ["Yellowing of leaves", "Stunted growth", "Hopperburn"],
                        "treatment": ["Imidacloprid 17.8% SL", "Neem oil spray"],
                        "prevention": ["Resistant varieties", "Proper spacing"]
                    },
                    "stem_borer": {
                        "symptoms": ["Dead hearts", "White ears", "Holes in stem"],
                        "treatment": ["Cartap hydrochloride", "Chlorantraniliprole"],
                        "prevention": ["Pheromone traps", "Early planting"]
                    }
                },
                "diseases": {
                    "blast": {
                        "symptoms": ["Diamond-shaped lesions", "Leaf blight", "Neck rot"],
                        "treatment": ["Tricyclazole", "Carbendazim"],
                        "prevention": ["Resistant varieties", "Balanced fertilization"]
                    },
                    "bacterial_blight": {
                        "symptoms": ["Water-soaked lesions", "Yellow halo", "Leaf death"],
                        "treatment": ["Copper oxychloride", "Streptomycin"],
                        "prevention": ["Clean seed", "Crop rotation"]
                    }
                }
            },
            "wheat": {
                "pests": {
                    "aphid": {
                        "symptoms": ["Yellowing leaves", "Sticky honeydew", "Stunted growth"],
                        "treatment": ["Imidacloprid", "Dimethoate"],
                        "prevention": ["Early sowing", "Resistant varieties"]
                    }
                },
                "diseases": {
                    "rust": {
                        "symptoms": ["Orange pustules", "Leaf yellowing", "Reduced yield"],
                        "treatment": ["Propiconazole", "Tebuconazole"],
                        "prevention": ["Resistant varieties", "Timely sowing"]
                    }
                }
            },
            "cotton": {
                "pests": {
                    "bollworm": {
                        "symptoms": ["Holes in bolls", "Larval damage", "Yield loss"],
                        "treatment": ["Bt cotton", "Spinosad", "Emamectin benzoate"],
                        "prevention": ["Pheromone traps", "Crop monitoring"]
                    },
                    "whitefly": {
                        "symptoms": ["Yellowing leaves", "Sooty mold", "Leaf curl"],
                        "treatment": ["Imidacloprid", "Thiamethoxam"],
                        "prevention": ["Yellow sticky traps", "Reflective mulch"]
                    }
                }
            }
        }
    
    async def process(self, query: str, context: Dict = None) -> AgentResponse:
        """Process pest and disease queries"""
        
        # Extract crop and symptoms
        crop = self._extract_crop(query, context)
        symptoms = self._extract_symptoms(query)
        pest_disease = self._identify_pest_disease(crop, symptoms, query)
        
        # Generate diagnosis and treatment plan
        diagnosis = self._generate_diagnosis(crop, pest_disease, symptoms)
        
        # Use Groq for detailed treatment recommendations
        groq_prompt = f"""
        As a plant pathologist and entomologist, provide comprehensive pest/disease management advice for:
        
        Crop: {crop}
        Symptoms observed: {symptoms}
        Suspected issue: {pest_disease}
        Query: {query}
        
        Provide detailed guidance on:
        1. Accurate diagnosis confirmation
        2. Immediate treatment measures
        3. Organic and chemical control options
        4. Prevention strategies for future
        5. Integrated Pest Management (IPM) approach
        6. Safety precautions for chemical use
        
        Include specific product names, dosages, and application methods.
        """
        
        groq_response = await self.groq_service.generate_response(groq_prompt)
        
        # Format response
        response_text = self._format_pest_disease_response(diagnosis, groq_response)
        
        return AgentResponse(
            agent_name=self.name,
            response=response_text,
            confidence=0.82,
            metadata={
                "crop": crop,
                "symptoms": symptoms,
                "suspected_issue": pest_disease,
                "treatment_urgency": diagnosis.get("urgency", "medium"),
                "organic_options": diagnosis.get("organic_treatments", [])
            },
            citations=["ICAR-IARI", "State Agricultural Universities", "IPM Guidelines"]
        )
    
    def _extract_crop(self, query: str, context: Dict = None) -> str:
        """Extract crop from query or context"""
        if context and context.get("crop_type"):
            return context["crop_type"]
        
        query_lower = query.lower()
        crops = ["rice", "wheat", "cotton", "maize", "sugarcane", "soybean", "tomato", "potato"]
        
        for crop in crops:
            if crop in query_lower:
                return crop
        
        return "general"
    
    def _extract_symptoms(self, query: str) -> List[str]:
        """Extract symptoms from query"""
        query_lower = query.lower()
        
        symptom_keywords = {
            "yellowing": ["yellow", "yellowing", "chlorosis"],
            "spots": ["spots", "lesions", "patches", "marks"],
            "wilting": ["wilting", "drooping", "sagging"],
            "holes": ["holes", "damage", "eaten", "chewed"],
            "stunted": ["stunted", "dwarf", "small", "reduced growth"],
            "death": ["death", "dying", "dead", "necrosis"],
            "insects": ["insects", "bugs", "pests", "larvae", "caterpillars"],
            "mold": ["mold", "fungus", "powdery", "fuzzy"]
        }
        
        symptoms = []
        for symptom, keywords in symptom_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                symptoms.append(symptom)
        
        return symptoms
    
    def _identify_pest_disease(self, crop: str, symptoms: List[str], query: str) -> str:
        """Identify most likely pest or disease"""
        if crop not in self.pest_disease_db:
            return "unknown"
        
        crop_data = self.pest_disease_db[crop]
        best_match = None
        best_score = 0
        
        # Check pests
        for pest_name, pest_info in crop_data.get("pests", {}).items():
            score = self._calculate_symptom_match(symptoms, pest_info["symptoms"], query)
            if score > best_score:
                best_score = score
                best_match = f"pest_{pest_name}"
        
        # Check diseases
        for disease_name, disease_info in crop_data.get("diseases", {}).items():
            score = self._calculate_symptom_match(symptoms, disease_info["symptoms"], query)
            if score > best_score:
                best_score = score
                best_match = f"disease_{disease_name}"
        
        return best_match or "unknown"
    
    def _calculate_symptom_match(self, observed_symptoms: List[str], known_symptoms: List[str], query: str) -> float:
        """Calculate how well symptoms match"""
        if not observed_symptoms:
            return 0.0
        
        query_lower = query.lower()
        match_score = 0
        
        for known_symptom in known_symptoms:
            known_lower = known_symptom.lower()
            # Direct keyword match
            if any(obs in known_lower or known_lower in obs for obs in observed_symptoms):
                match_score += 1
            # Query text match
            elif any(word in query_lower for word in known_lower.split()):
                match_score += 0.5
        
        return match_score / len(known_symptoms)
    
    def _generate_diagnosis(self, crop: str, pest_disease: str, symptoms: List[str]) -> Dict:
        """Generate diagnosis information"""
        diagnosis = {
            "crop": crop,
            "issue_type": "unknown",
            "confidence": 0.5,
            "urgency": "medium",
            "treatments": [],
            "organic_treatments": [],
            "prevention": []
        }
        
        if pest_disease == "unknown" or crop not in self.pest_disease_db:
            return diagnosis
        
        crop_data = self.pest_disease_db[crop]
        issue_type, issue_name = pest_disease.split("_", 1)
        
        if issue_type == "pest" and issue_name in crop_data.get("pests", {}):
            pest_info = crop_data["pests"][issue_name]
            diagnosis.update({
                "issue_type": "pest",
                "issue_name": issue_name.replace("_", " ").title(),
                "confidence": 0.8,
                "treatments": pest_info["treatment"],
                "prevention": pest_info["prevention"],
                "urgency": "high" if "borer" in issue_name or "bollworm" in issue_name else "medium"
            })
        elif issue_type == "disease" and issue_name in crop_data.get("diseases", {}):
            disease_info = crop_data["diseases"][issue_name]
            diagnosis.update({
                "issue_type": "disease",
                "issue_name": issue_name.replace("_", " ").title(),
                "confidence": 0.8,
                "treatments": disease_info["treatment"],
                "prevention": disease_info["prevention"],
                "urgency": "high" if "blight" in issue_name or "rust" in issue_name else "medium"
            })
        
        # Add organic alternatives
        organic_alternatives = {
            "neem oil": "Neem oil spray (5ml/L water)",
            "bt spray": "Bacillus thuringiensis spray",
            "copper fungicide": "Copper sulfate solution",
            "trichoderma": "Trichoderma viride application"
        }
        
        diagnosis["organic_treatments"] = list(organic_alternatives.values())[:3]
        
        return diagnosis
    
    def _format_pest_disease_response(self, diagnosis: Dict, groq_response: str) -> str:
        """Format pest and disease management response"""
        
        response = "🐛 **Pest & Disease Diagnosis**\n\n"
        
        if diagnosis["issue_type"] != "unknown":
            urgency_emoji = "🚨" if diagnosis["urgency"] == "high" else "⚠️"
            response += f"**Suspected Issue:** {diagnosis['issue_name']}\n"
            response += f"**Type:** {diagnosis['issue_type'].title()}\n"
            response += f"**Urgency:** {urgency_emoji} {diagnosis['urgency'].title()}\n"
            response += f"**Confidence:** {int(diagnosis['confidence'] * 100)}%\n\n"
            
            # Treatment options
            if diagnosis["treatments"]:
                response += f"**Recommended Treatments:**\n"
                for i, treatment in enumerate(diagnosis["treatments"], 1):
                    response += f"{i}. {treatment}\n"
                response += "\n"
            
            # Organic alternatives
            if diagnosis["organic_treatments"]:
                response += f"**Organic Alternatives:**\n"
                for i, organic in enumerate(diagnosis["organic_treatments"], 1):
                    response += f"{i}. {organic}\n"
                response += "\n"
            
            # Prevention measures
            if diagnosis["prevention"]:
                response += f"**Prevention for Future:**\n"
                for i, prevention in enumerate(diagnosis["prevention"], 1):
                    response += f"{i}. {prevention}\n"
                response += "\n"
        else:
            response += "**Status:** Unable to identify specific issue from description\n\n"
            response += "**Recommendation:** Please provide more detailed symptoms or consult local agricultural extension officer\n\n"
        
        # Add detailed Groq recommendations
        response += f"**Detailed Management Plan:**\n{groq_response}\n\n"
        
        # Safety note
        response += f"**⚠️ Safety Note:** Always read and follow pesticide labels. Use protective equipment when applying chemicals. Consider IPM approach for sustainable management."
        
        return response