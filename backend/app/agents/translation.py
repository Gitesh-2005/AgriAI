import json
from typing import Dict, List
from app.agents.base import BaseAgent, AgentResponse

class TranslationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Translation",
            description="Translates agricultural content between English and Indian regional languages"
        )
        
        # Agricultural terminology dictionary
        self.agri_terms = {
            "en_to_hi": {
                "farmer": "किसान",
                "crop": "फसल",
                "soil": "मिट्टी",
                "water": "पानी",
                "fertilizer": "उर्वरक",
                "seed": "बीज",
                "harvest": "फसल कटाई",
                "irrigation": "सिंचाई",
                "pest": "कीट",
                "disease": "रोग",
                "weather": "मौसम",
                "rain": "बारिश",
                "drought": "सूखा",
                "flood": "बाढ़",
                "market": "बाजार",
                "price": "कीमत",
                "subsidy": "सब्सिडी",
                "loan": "ऋण",
                "insurance": "बीमा",
                "rice": "चावल",
                "wheat": "गेहूं",
                "cotton": "कपास",
                "sugarcane": "गन्ना",
                "maize": "मक्का"
            },
            "hi_to_en": {
                "किसान": "farmer",
                "फसल": "crop",
                "मिट्टी": "soil",
                "पानी": "water",
                "उर्वरक": "fertilizer",
                "बीज": "seed",
                "फसल कटाई": "harvest",
                "सिंचाई": "irrigation",
                "कीट": "pest",
                "रोग": "disease",
                "मौसम": "weather",
                "बारिश": "rain",
                "सूखा": "drought",
                "बाढ़": "flood",
                "बाजार": "market",
                "कीमत": "price",
                "सब्सिडी": "subsidy",
                "ऋण": "loan",
                "बीमा": "insurance",
                "चावल": "rice",
                "गेहूं": "wheat",
                "कपास": "cotton",
                "गन्ना": "sugarcane",
                "मक्का": "maize"
            }
        }
        
        # Common agricultural phrases
        self.common_phrases = {
            "en_to_hi": {
                "How is your crop?": "आपकी फसल कैसी है?",
                "What is the weather today?": "आज मौसम कैसा है?",
                "When should I sow seeds?": "मुझे बीज कब बोना चाहिए?",
                "What is the market price?": "बाजार भाव क्या है?",
                "How much fertilizer should I use?": "मुझे कितना उर्वरक इस्तेमाल करना चाहिए?",
                "Is there any government scheme?": "क्या कोई सरकारी योजना है?",
                "My crop is affected by pests": "मेरी फसल में कीट लगे हैं",
                "I need irrigation advice": "मुझे सिंचाई की सलाह चाहिए"
            },
            "hi_to_en": {
                "आपकी फसल कैसी है?": "How is your crop?",
                "आज मौसम कैसा है?": "What is the weather today?",
                "मुझे बीज कब बोना चाहिए?": "When should I sow seeds?",
                "बाजार भाव क्या है?": "What is the market price?",
                "मुझे कितना उर्वरक इस्तेमाल करना चाहिए?": "How much fertilizer should I use?",
                "क्या कोई सरकारी योजना है?": "Is there any government scheme?",
                "मेरी फसल में कीट लगे हैं": "My crop is affected by pests",
                "मुझे सिंचाई की सलाह चाहिए": "I need irrigation advice"
            }
        }
    
    async def process(self, query: str, context: Dict = None) -> AgentResponse:
        """Process translation queries"""
        
        # Detect source and target languages
        source_lang, target_lang = self._detect_languages(query, context)
        
        # Extract text to translate
        text_to_translate = self._extract_text_to_translate(query)
        
        # Perform translation
        translated_text = self._translate_text(text_to_translate, source_lang, target_lang)
        
        # Format response
        response_text = self._format_translation_response(
            text_to_translate, translated_text, source_lang, target_lang
        )
        
        return AgentResponse(
            agent_name=self.name,
            response=response_text,
            confidence=0.8,
            metadata={
                "source_language": source_lang,
                "target_language": target_lang,
                "original_text": text_to_translate,
                "translated_text": translated_text,
                "translation_method": "dictionary_based"
            },
            citations=["Agricultural Terminology Dictionary", "Common Farming Phrases"]
        )
    
    def _detect_languages(self, query: str, context: Dict = None) -> tuple:
        """Detect source and target languages"""
        
        # Check context for language preferences
        if context:
            user_lang = context.get("language", "en")
            if user_lang == "hi":
                return "hi", "en"  # Hindi to English
            else:
                return "en", "hi"  # English to Hindi
        
        # Simple detection based on script
        if self._contains_devanagari(query):
            return "hi", "en"
        else:
            return "en", "hi"
    
    def _contains_devanagari(self, text: str) -> bool:
        """Check if text contains Devanagari script"""
        for char in text:
            if '\u0900' <= char <= '\u097F':  # Devanagari Unicode range
                return True
        return False
    
    def _extract_text_to_translate(self, query: str) -> str:
        """Extract the actual text to translate from query"""
        
        # Remove common translation request phrases
        translation_indicators = [
            "translate", "translation", "convert", "meaning", "hindi", "english",
            "अनुवाद", "मतलब", "अर्थ"
        ]
        
        words = query.split()
        filtered_words = []
        
        for word in words:
            if word.lower() not in translation_indicators:
                filtered_words.append(word)
        
        # If no meaningful text remains, use original query
        if not filtered_words:
            return query
        
        return " ".join(filtered_words)
    
    def _translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text using dictionary and phrase matching"""
        
        # Check for exact phrase matches first
        phrase_dict = f"{source_lang}_to_{target_lang}"
        if phrase_dict in self.common_phrases:
            for phrase, translation in self.common_phrases[phrase_dict].items():
                if phrase.lower() in text.lower():
                    return translation
        
        # Word-by-word translation for agricultural terms
        term_dict = f"{source_lang}_to_{target_lang}"
        if term_dict in self.agri_terms:
            words = text.split()
            translated_words = []
            
            for word in words:
                # Clean word (remove punctuation)
                clean_word = word.strip(".,!?()[]{}\"'")
                
                # Check if it's an agricultural term
                if clean_word.lower() in self.agri_terms[term_dict]:
                    translated_words.append(self.agri_terms[term_dict][clean_word.lower()])
                elif clean_word in self.agri_terms[term_dict]:
                    translated_words.append(self.agri_terms[term_dict][clean_word])
                else:
                    # Keep original word if no translation found
                    translated_words.append(word)
            
            return " ".join(translated_words)
        
        # If no translation possible, return original with note
        return f"{text} (Translation not available - please use simpler agricultural terms)"
    
    def _format_translation_response(self, original: str, translated: str, 
                                   source_lang: str, target_lang: str) -> str:
        """Format translation response"""
        
        lang_names = {
            "en": "English",
            "hi": "Hindi (हिंदी)"
        }
        
        response = "🌐 **Translation Service**\n\n"
        response += f"**Original ({lang_names[source_lang]}):** {original}\n\n"
        response += f"**Translation ({lang_names[target_lang]}):** {translated}\n\n"
        
        # Add helpful agricultural terms
        response += "**Common Agricultural Terms:**\n"
        
        if source_lang == "en":
            sample_terms = [
                ("Farmer", "किसान"),
                ("Crop", "फसल"),
                ("Soil", "मिट्टी"),
                ("Water", "पानी"),
                ("Fertilizer", "उर्वरक")
            ]
        else:
            sample_terms = [
                ("किसान", "Farmer"),
                ("फसल", "Crop"),
                ("मिट्टी", "Soil"),
                ("पानी", "Water"),
                ("उर्वरक", "Fertilizer")
            ]
        
        for term1, term2 in sample_terms:
            response += f"• {term1} = {term2}\n"
        
        response += "\n**💡 Tip:** For better translations, use simple agricultural terms and phrases."
        
        return response
    
    async def translate_response(self, text: str, target_language: str) -> str:
        """Translate AI response to target language"""
        
        if target_language == "hi":
            # Translate key agricultural terms in the response
            translated_text = text
            
            for en_term, hi_term in self.agri_terms["en_to_hi"].items():
                # Case-insensitive replacement
                import re
                pattern = re.compile(re.escape(en_term), re.IGNORECASE)
                translated_text = pattern.sub(hi_term, translated_text)
            
            return translated_text
        
        return text  # Return original if target is English or unsupported