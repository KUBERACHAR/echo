"""
backend/gemini_service.py
Gemini LLM Service for Personalized Mental Wellness Assistance.

Integrates Google Gemini to deliver empathetic, evidence-informed,
personalized wellness guidance adapted to the user's real-time detected
facial emotions, stress scores, and conversational context in multiple
languages (English, Kannada, Hindi, Telugu).
"""

import os
import sys
import json
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Import developer config
try:
    import config
    CONFIG_API_KEY = getattr(config, "GEMINI_API_KEY", "")
    CONFIG_DEFAULT_MODEL = getattr(config, "DEFAULT_GEMINI_MODEL", "gemini-1.5-flash")
    CONFIG_DEFAULT_TEMP = getattr(config, "DEFAULT_TEMPERATURE", 0.7)
except ImportError:
    CONFIG_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    CONFIG_DEFAULT_MODEL = "gemini-1.5-flash"
    CONFIG_DEFAULT_TEMP = 0.7

# Default system instruction for Mental Wellness Assistant
SYSTEM_PROMPT = """You are "MindCare Companion", a compassionate, warm, empathetic, and evidence-informed Personalized Mental Wellness Assistant.
Your mission is to provide comforting support, practical stress-relief techniques, mindfulness guidance, and reflective conversation to help users maintain emotional well-being.

KEY BEHAVIORS:
1. Warm & Non-Judgmental: Meet the user with deep compassion, validation, and active listening. Always make them feel heard and respected.
2. Context-Aware Personalization:
   - When provided with real-time detected facial emotion, stress level, and confidence, naturally and delicately reference this state.
   - For High Stress / Fear / Anger / Sadness: Gently acknowledge their tension, validate their feelings, and offer calming grounding exercises (e.g., 4-7-8 breathing, box breathing, 5-4-3-2-1 sensory grounding, gentle progressive relaxation).
   - For Calm / Happiness: Celebrate their positive mental state, encourage savoring positive moments, gratitude, and sustainable balance.
   - Never sound clinical, accusatory, or robotic about their detected expressions.
3. Practical & Actionable: Give clear, gentle, step-by-step suggestions when appropriate (e.g., a 2-minute breathing exercise, physical posture reset, sipping warm water, taking a brief screen break).
4. Clarity & Formatting: Keep responses conversational, concise, and beautifully formatted with bullet points, brief paragraphs, and soothing emojis. Avoid overwhelming walls of text.
5. Safety Protocol & Disclaimer:
   - You are a wellness companion, NOT a medical doctor or licensed psychotherapist. You do not diagnose conditions or prescribe medications.
   - If the user indicates extreme emotional crisis, despair, or self-harm/suicide risk:
     Respond with deep unconditional warmth and immediately urge them to connect with professional help. Provide emergency crisis lines:
     * USA & Canada: Call or text 988 (Suicide & Crisis Lifeline)
     * UK: Call 111 or text SHOUT to 85258
     * India: Tele-MANAS (14416 / 1800-891-4416) or Vandrevala Foundation (9999 666 555)
     * International: https://findahelpline.com
"""

class GeminiWellnessAssistant:
    """Service to interact with Google Gemini models for mental wellness support."""

    AVAILABLE_MODELS = [
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemini-3.8-flash",
        "gemini-2.5-flash-lite",
        "gemini-1.5-flash",
    ]
    DEFAULT_MODEL = "gemini-3.5-flash-lite"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ):
        self.api_key = (api_key or CONFIG_API_KEY or os.environ.get("GEMINI_API_KEY", "")).strip()
        selected_model = model or CONFIG_DEFAULT_MODEL or self.DEFAULT_MODEL
        self.model = selected_model if selected_model in self.AVAILABLE_MODELS else self.DEFAULT_MODEL
        temp = temperature if temperature is not None else CONFIG_DEFAULT_TEMP
        self.temperature = max(0.0, min(1.0, float(temp)))

    def set_api_key(self, api_key: str):
        """Update active API key."""
        self.api_key = (api_key or "").strip()

    def set_model(self, model: str):
        """Update active model."""
        if model in self.AVAILABLE_MODELS:
            self.model = model

    def set_temperature(self, temperature: float):
        """Update temperature."""
        self.temperature = max(0.0, min(1.0, temperature))

    def is_configured(self) -> bool:
        """Check if a valid developer API key is provided."""
        return bool(
            self.api_key
            and self.api_key != "YOUR_GEMINI_API_KEY_HERE"
            and len(self.api_key) > 10
        )

    def test_connection(self) -> Tuple[bool, str]:
        """Test API connectivity with automatic model fallback."""
        if not self.is_configured():
            return False, "API key is not configured in config.py or .env."
        
        import requests
        models_to_test = [self.model] + [m for m in self.AVAILABLE_MODELS if m != self.model]
        last_msg = ""
        for m in models_to_test:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={self.api_key}"
                payload = {
                    "contents": [{"role": "user", "parts": [{"text": "Ping"}]}],
                    "generationConfig": {"maxOutputTokens": 5}
                }
                res = requests.post(url, json=payload, timeout=12)
                if res.status_code == 200:
                    self.model = m
                    return True, f"Successfully connected to Gemini API (using {m})!"
                
                err_info = res.json().get("error", {})
                last_msg = err_info.get("message", f"HTTP {res.status_code}")
                if res.status_code in [404, 503]:
                    continue  # Try next active model
                else:
                    return False, f"API Error ({res.status_code}): {last_msg}"
            except Exception as e:
                last_msg = str(e)
                continue
                
        return False, f"Connection failed: {last_msg}"

    def generate_wellness_response(
        self,
        user_message: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        emotion_context: Optional[Dict[str, any]] = None,
        language: str = "English",
    ) -> str:
        """
        Generate personalized mental wellness response using Gemini API with auto-fallback.
        Supports multi-language outputs (English, Kannada, Hindi, Telugu).
        """
        if not self.is_configured():
            return self._generate_fallback_response(user_message, emotion_context, language)

        # Build language-specific guidance
        language_instructions = {
            "English": "Respond entirely in English. Maintain an empathetic, warm, and comforting tone.",
            "Kannada": (
                "You MUST respond ENTIRELY in natural, grammatically correct, polite Kannada using Kannada script (ಕನ್ನಡ ಲಿಪಿಯಲ್ಲಿ ಉತ್ತರಿಸಿ). "
                "Do not use Latin/English script for your sentences. Maintain deep warmth, empathy, and cultural respect."
            ),
            "Hindi": (
                "You MUST respond ENTIRELY in natural, polite Hindi using Devanagari script (हिन्दी / देवनागरी लिपि में उत्तर दें). "
                "Do not use Romanized Hinglish. Maintain deep warmth, empathy, and comfort."
            ),
            "Telugu": (
                "You MUST respond ENTIRELY in natural, polite Telugu using Telugu script (తెలుగు లిపిలో సమాధానం ఇవ్వండి). "
                "Do not use Latin/English script for your sentences. Maintain warmth, encouragement, and empathetic care."
            )
        }
        lang_instruction = language_instructions.get(language, f"Respond in {language}.")
        full_system_prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"CRITICAL LANGUAGE INSTRUCTION:\n"
            f"- User Selected Language: **{language}**\n"
            f"- {lang_instruction}\n"
            f"- All reflections, breathing exercises, affirmations, and suggestions MUST be in {language}."
        )

        # Prepare payload for Gemini API
        contents = self._prepare_contents(user_message, chat_history, emotion_context, language)
        
        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": full_system_prompt}]
            },
            "generationConfig": {
                "temperature": self.temperature,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }

        import requests
        models_to_try = [self.model] + [m for m in self.AVAILABLE_MODELS if m != self.model]
        last_error = ""

        for candidate_model in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{candidate_model}:generateContent?key={self.api_key}"
                response = requests.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload),
                    timeout=25
                )

                # If systemInstruction caused a 400 with older models, fallback without it
                if response.status_code == 400:
                    err_data = response.json().get("error", {})
                    err_msg = err_data.get("message", "")
                    if "systemInstruction" in err_msg or "system_instruction" in err_msg:
                        alt_payload = dict(payload)
                        alt_payload.pop("systemInstruction", None)
                        alt_contents = list(contents)
                        if alt_contents and alt_contents[0]["role"] == "user":
                            alt_contents[0] = {
                                "role": "user",
                                "parts": [{"text": f"[System Instruction: {full_system_prompt}]\n\n" + alt_contents[0]["parts"][0]["text"]}]
                            }
                        alt_payload["contents"] = alt_contents
                        response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(alt_payload), timeout=25)

                if response.status_code == 200:
                    self.model = candidate_model  # update active model
                    data = response.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"].strip()
                    fallback_msgs = {
                        "Kannada": "ನಾನು ನಿಮ್ಮ ಮಾತನ್ನು ಕೇಳುತ್ತಿದ್ದೇನೆ, ಆದರೆ ಈ ಕ್ಷಣದಲ್ಲಿ ಉತ್ತರವನ್ನು ರಚಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ನಿಮ್ಮ ಕ್ಷೇಮಕ್ಕೆ ನಾನು ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ?",
                        "Hindi": "मैं आपकी बात सुन रहा हूँ, लेकिन अभी उत्तर तैयार नहीं कर सका। मैं आपकी कैसे मदद कर सकता हूँ?",
                        "Telugu": "నేను వింటున్నాను, కానీ ప్రస్తుతానికి సమాధానం సిద్ధం చేయలేకపోయాను. నేను మీకు ఎలా సహాయపడగలను?",
                        "English": "I'm listening, but I couldn't formulate a response right now. How else can I support your wellness?"
                    }
                    return fallback_msgs.get(language, fallback_msgs["English"])

                # If 404 (model deprecated/not found) or 503 (model overloaded), try next model
                if response.status_code in [404, 503]:
                    err_info = response.json().get("error", {})
                    last_error = f"Model {candidate_model} returned {response.status_code}: {err_info.get('message', '')}"
                    continue

                # Handle specific error status codes
                if response.status_code == 400:
                    err = response.json().get("error", {})
                    return f"⚠️ **Gemini API Error (400):** {err.get('message', 'Invalid request or invalid API key.')}\nPlease verify your API key."
                elif response.status_code == 403:
                    return "⚠️ **Access Denied (403):** The API key provided does not have permissions to access Gemini or has expired."
                elif response.status_code == 429:
                    return "⏳ **Rate Limit Exceeded (429):** Your Gemini API rate limit or free tier quota has been reached. Please pause for a moment before trying again."
                else:
                    err_msg = response.json().get("error", {}).get("message", response.text[:200])
                    return f"⚠️ **Service Notice ({response.status_code}):** {err_msg}"

            except Exception as e:
                logger.error(f"Error calling Gemini model {candidate_model}: {e}")
                last_error = str(e)
                continue

        return f"⚠️ **Gemini Error:** Unable to reach models. Details: {last_error}\n\n*In the meantime, take a deep breath in for 4 seconds, hold for 4 seconds, and exhale for 6 seconds.*"

    def _prepare_contents(
        self,
        latest_message: str,
        chat_history: Optional[List[Dict[str, str]]],
        emotion_context: Optional[Dict[str, any]],
        language: str = "English",
    ) -> List[Dict]:
        """Format chat history into alternating user/model turns for Gemini."""
        contents = []

        if chat_history:
            for msg in chat_history:
                role = "user" if msg.get("role") == "user" else "model"
                text = msg.get("content", "").strip()
                if not text:
                    continue
                # Avoid consecutive identical roles
                if contents and contents[-1]["role"] == role:
                    contents[-1]["parts"][0]["text"] += f"\n\n{text}"
                else:
                    contents.append({"role": role, "parts": [{"text": text}]})

        # Inject real-time emotional telemetry into current turn
        context_prefix = f"[User Language Preference: {language}]\n"
        if emotion_context and emotion_context.get("emotion") and emotion_context.get("emotion") != "None":
            emotion = emotion_context.get("emotion", "Unknown").capitalize()
            stress = emotion_context.get("stress", "Unknown")
            conf = emotion_context.get("confidence", 0)
            context_prefix += (
                f"[Real-Time Wellness Context: Facial Emotion = {emotion}, "
                f"Estimated Stress Level = {stress}, Model Confidence = {conf}%]\n\n"
            )

        full_user_text = context_prefix + latest_message

        # Ensure alternating role and ends with user
        if contents and contents[-1]["role"] == "user":
            contents[-1]["parts"][0]["text"] += f"\n\n{full_user_text}"
        else:
            contents.append({"role": "user", "parts": [{"text": full_user_text}]})

        # Gemini requires the first turn to be 'user'
        if contents and contents[0]["role"] != "user":
            contents.pop(0)

        return contents

    def _generate_fallback_response(
        self,
        user_message: str,
        emotion_context: Optional[Dict[str, any]],
        language: str = "English",
    ) -> str:
        """
        Graceful response when Gemini API key is not yet configured.
        Provides immediate wellness support and guides user on setting the key in selected language.
        """
        emotion = (emotion_context.get("emotion", "") if emotion_context else "").lower()
        stress = (emotion_context.get("stress", "") if emotion_context else "").lower()

        is_high = "high" in stress or emotion in ["angry", "fear", "sad"]
        is_happy = emotion in ["happy", "surprise"]

        if language == "Kannada":
            if is_high:
                tip = (
                    "🌿 **ತಕ್ಷಣದ ಒತ್ತಡ ಪರಿಹಾರ ವ್ಯಾಯಾಮಗಳು:**\n"
                    "• **ಬಾಕ್ಸ್ ಬ್ರೀತಿಂಗ್ (ಉಸಿರಾಟ):** 4 ಸೆಕೆಂಡುಗಳ ಕಾಲ ಉಸಿರನ್ನು ಒಳಗೆ ತೆಗೆದುಕೊಳ್ಳಿ, 4 ಸೆಕೆಂಡುಗಳ ಕಾಲ ಹಿಡಿದುಕೊಳ್ಳಿ, 4 ಸೆಕೆಂಡುಗಳಲ್ಲಿ ಹೊರಬಿಡಿ, 4 ಸೆಕೆಂಡು ಕಾಯಿರಿ. ಇದನ್ನು 3 ಬಾರಿ ಪುನರಾವರ್ತಿಸಿ.\n"
                    "• **ನೆಲಸುವಿಕೆ (ಗ್ರೌಂಡಿಂಗ್):** ನಿಮ್ಮ ಸುತ್ತಲೂ ಕಾಣುವ 5 ವಸ್ತುಗಳು, ಸ್ಪರ್ಶಿಸಬಹುದಾದ 4 ವಸ್ತುಗಳು ಮತ್ತು ಕೇಳುವ 3 ಧ್ವನಿಗಳನ್ನು ಗಮನಿಸಿ.\n"
                    "• **ಭಂಗಿ (Posture):** ನಿಮ್ಮ ಭುಜಗಳನ್ನು ಸಡಿಲಗೊಳಿಸಿ ಮತ್ತು ದವಡೆಯ ಒತ್ತಡವನ್ನು ಸಡಿಲಗೊಳಿಸಿ.\n\n"
                )
            elif is_happy:
                tip = (
                    "✨ **ಈ ಕ್ಷಣವನ್ನು ಆನಂದಿಸಿ:**\n"
                    "• ನೀವು ಪ್ರಸ್ತುತ ಅನುಭವಿಸುತ್ತಿರುವ ಸಕಾರಾತ್ಮಕ ಶಕ್ತಿಯನ್ನು ಪ್ರಶಂಸಿಸಲು ಒಂದು ಕ್ಷಣ ತೆಗೆದುಕೊಳ್ಳಿ.\n"
                    "• ಇಂದಿನ ದಿನದಲ್ಲಿ ನೀವು ಕೃತಜ್ಞರಾಗಿರುವ ಒಂದು ವಿಷಯ ಯಾವುದು?\n\n"
                )
            else:
                tip = (
                    "🧘 **ಮನಸ್ಸಿನ ಶಾಂತಿ:**\n"
                    "• ಆರಾಮವಾಗಿ ಕುಳಿತು ಆಳವಾದ, ನಿಧಾನವಾದ ಉಸಿರನ್ನು ತೆಗೆದುಕೊಳ್ಳಿ.\n"
                    "• ಕುತ್ತಿಗೆ, ಭುಜ ಮತ್ತು ಹಣೆಯ ಮೇಲಿನ ಎಲ್ಲಾ ಒತ್ತಡವನ್ನು ಮುಕ್ತಗೊಳಿಸಿ.\n\n"
                )
            return (
                f"ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ **ವೈಯಕ್ತಿಕ ಮಾನಸಿಕ ಕ್ಷೇಮ ಸಹಾಯಕ**.\n\n"
                f"{tip}"
                f"ನಿಮ್ಮ ಮಾನಸಿಕ ಆರೋಗ್ಯ, ಒತ್ತಡ ನಿರ್ವಹಣೆ ಮತ್ತು ದೈನಂದಿನ ಯೋಗಕ್ಷೇಮಕ್ಕೆ ಬೆಂಬಲ ನೀಡಲು ನಾನಿದ್ದೇನೆ. "
                f"ನಿಮ್ಮ ಮನಸ್ಸಿನಲ್ಲಿರುವುದನ್ನು ಹಂಚಿಕೊಳ್ಳಿ ಅಥವಾ ಮೇಲಿನ ತ್ವರಿತ ಕ್ಷೇಮ ವ್ಯಾಯಾಮಗಳಲ್ಲಿ ಒಂದನ್ನು ಆರಿಸಿ!\n\n"
                f"---\n"
                f"*(ಡೆವಲಪರ್ ಸೂಚನೆ: Google Gemini ಯಿಂದ ನೇರ AI ಪ್ರತಿಕ್ರಿಯೆಗಳನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಲು, ದಯವಿಟ್ಟು `config.py` ಅಥವಾ `.env` ನಲ್ಲಿ ನಿಮ್ಮ `GEMINI_API_KEY` ಅನ್ನು ನಮೂದಿಸಿ)*"
            )

        elif language == "Hindi":
            if is_high:
                tip = (
                    "🌿 **तत्काल तनाव राहत अभ्यास:**\n"
                    "• **बॉक्स ब्रीदिंग:** 4 सेकंड सांस अंदर लें, 4 सेकंड रोकें, 4 सेकंड में सांस छोड़ें, 4 सेकंड रुकें। इसे 3 बार दोहराएं।\n"
                    "• **ग्राउंडिंग:** अपने आस-पास दिखने वाली 5 चीजें, 4 चीजें जिन्हें आप छू सकते हैं, और 3 आवाजें जो आप सुन सकते हैं, उन पर ध्यान दें।\n"
                    "• **मुद्रा:** अपने कंधों को ढीला करें और जबड़े के तनाव को छोड़ें।\n\n"
                )
            elif is_happy:
                tip = (
                    "✨ **सकारात्मक पल को संजोएं:**\n"
                    "• इस समय आप जो सकारात्मक ऊर्जा महसूस कर रहे हैं, उसे महसूस करने के लिए एक क्षण निकालें।\n"
                    "• आज ऐसी कौन सी बात है जिसके लिए आप आभारी हैं?\n\n"
                )
            else:
                tip = (
                    "🧘 **माइंडफुल रीसेट:**\n"
                    "• आराम से बैठें और एक गहरी, धीमी सांस लें।\n"
                    "• अपने माथे, गर्दन और कंधों के तनाव को पूरी तरह छोड़ दें।\n\n"
                )
            return (
                f"नमस्ते! मैं आपका **व्यक्तिगत मानसिक स्वास्थ्य सहायक** हूँ।\n\n"
                f"{tip}"
                f"मैं आपके मानसिक स्वास्थ्य, तनाव प्रबंधन और दैनिक कल्याण का समर्थन करने के लिए यहाँ हूँ। "
                f"बेझिझक अपने विचार साझा करें या ऊपर दिए गए त्वरित अभ्यासों में से एक चुनें!\n\n"
                f"---\n"
                f"*(डेवलपर सूचना: Google Gemini से लाइव प्रतिक्रियाएं सक्षम करने के लिए, कृपया `config.py` या `.env` में अपनी `GEMINI_API_KEY` दर्ज करें)*"
            )

        elif language == "Telugu":
            if is_high:
                tip = (
                    "🌿 **తక్షణ ఒత్తిడి ఉపశమన వ్యాయామాలు:**\n"
                    "• **బాక్స్ బ్రీతింగ్:** 4 సెకన్ల పాటు శ్వాస తీసుకోండి, 4 సెకన్లు ఆపండి, 4 సెకన్లలో వదలండి, 4 సెకన్లు ఆగండి. దీన్ని 3 సార్లు పునరావృతం చేయండి.\n"
                    "• **గ్రౌండింగ్:** మీ చుట్టూ కనిపించే 5 విషయాలు, మీరు తాకగల 4 విషయాలు, మీరు వినగల 3 శబ్దాలను గమనించండి.\n"
                    "• **భంగిమ:** మీ భుజాలను రిలాక్స్ చేయండి మరియు దవడ ఒత్తిడిని తగ్గించండి.\n\n"
                )
            elif is_happy:
                tip = (
                    "✨ **ఈ క్షణాన్ని ఆస్వాదించండి:**\n"
                    "• మీరు ప్రస్తుతం అనుభవిస్తున్న సానుకూల శక్తిని గుర్తించడానికి ఒక క్షణం తీసుకోండి.\n"
                    "• ఈ రోజు మీరు కృతజ్ఞతగా భావించే ఒక విషయం ఏమిటి?\n\n"
                )
            else:
                tip = (
                    "🧘 **మనస్సు ప్రశాంతత:**\n"
                    "• సౌకర్యవంతంగా కూర్చుని లోతైన, నెమ్మదిగా శ్వాస తీసుకోండి.\n"
                    "• నుదిటి, మెడ మరియు భుజాల వద్ద ఉన్న ఒత్తిడిని విడుదల చేయండి.\n\n"
                )
            return (
                f"నమస్కారం! నేను మీ **వ్యక్తిగతీకరించిన మానసిక శ్రేయస్సు సహాయకుడిని**.\n\n"
                f"{tip}"
                f"మీ మానసిక ఆరోగ్యం, ఒత్తిడి నిర్వహణ మరియు శ్రేయస్సుకు మద్దతు ఇవ్వడానికి నేను ఇక్కడ ఉన్నాను. "
                f"మీ మనస్సులోని విషయాలను నిస్సంకోచంగా పంచుకోండి లేదా పైన పేర్కొన్న శీఘ్ర వ్యాయామాలలో ఒకదాన్ని ఎంచుకోండి!\n\n"
                f"---\n"
                f"*(డెవలపర్ నోటీసు: Google Gemini ప్రత్యక్ష ప్రతిస్పందనలను ప్రారంభించడానికి, దయచేసి `config.py` లేదా `.env` లో మీ `GEMINI_API_KEY` ని నమోదు చేయండి)*"
            )

        else:  # English
            if is_high:
                wellness_tip = (
                    "🌿 **Immediate Stress Relief:**\n"
                    "• **Box Breathing:** Inhale for 4 seconds, hold for 4, exhale for 4, hold for 4. Repeat 3 times.\n"
                    "• **Grounding:** Notice 5 things you can see around you right now, 4 things you can touch, and 3 sounds you hear.\n"
                    "• **Posture:** Gently roll your shoulders back and unclench your jaw.\n\n"
                )
            elif is_happy:
                wellness_tip = (
                    "✨ **Savoring the Moment:**\n"
                    "• Take a moment to acknowledge the positive energy you're feeling right now.\n"
                    "• What is one thing you feel grateful for today?\n\n"
                )
            else:
                wellness_tip = (
                    "🧘 **Mindful Reset:**\n"
                    "• Sit comfortably and take a deep, slow breath.\n"
                    "• Release any tension in your forehead, neck, and shoulders.\n\n"
                )

            return (
                f"Hello! I am your **Personalized Mental Wellness Assistant**.\n\n"
                f"{wellness_tip}"
                f"I am here to support your mental health, stress management, and daily well-being. "
                f"Feel free to share what's on your mind or choose one of the quick wellness exercises above!\n\n"
                f"---\n"
                f"*(Developer notice: To enable live generative responses from Google Gemini, please define your `GEMINI_API_KEY` in `config.py` or `.env`)*"
            )
