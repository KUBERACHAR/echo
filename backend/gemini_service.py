"""
backend/gemini_service.py
Gemini LLM Service for Personalized Mental Wellness Assistance.

Integrates Google Gemini to deliver empathetic, evidence-informed,
personalized wellness guidance adapted to the user's real-time detected
facial emotions, stress scores, and conversational context.
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
    ) -> str:
        """
        Generate personalized mental wellness response using Gemini API with auto-fallback.
        """
        if not self.is_configured():
            return self._generate_fallback_response(user_message, emotion_context)

        # Prepare payload for Gemini API
        contents = self._prepare_contents(user_message, chat_history, emotion_context)
        
        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
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
                                "parts": [{"text": f"[System Instruction: {SYSTEM_PROMPT}]\n\n" + alt_contents[0]["parts"][0]["text"]}]
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
                    return "I'm listening, but I couldn't formulate a response right now. How else can I support your wellness?"

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
        emotion_context: Optional[Dict[str, any]]
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
        context_prefix = ""
        if emotion_context and emotion_context.get("emotion") and emotion_context.get("emotion") != "None":
            emotion = emotion_context.get("emotion", "Unknown").capitalize()
            stress = emotion_context.get("stress", "Unknown")
            conf = emotion_context.get("confidence", 0)
            context_prefix = (
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
        emotion_context: Optional[Dict[str, any]]
    ) -> str:
        """
        Graceful response when Gemini API key is not yet configured.
        Provides immediate wellness support and guides user on setting the key.
        """
        emotion = (emotion_context.get("emotion", "") if emotion_context else "").lower()
        stress = (emotion_context.get("stress", "") if emotion_context else "").lower()

        wellness_tip = ""
        if "high" in stress or emotion in ["angry", "fear", "sad"]:
            wellness_tip = (
                "🌿 **Immediate Stress Relief:**\n"
                "• **Box Breathing:** Inhale for 4 seconds, hold for 4, exhale for 4, hold for 4. Repeat 3 times.\n"
                "• **Grounding:** Notice 5 things you can see around you right now, 4 things you can touch, and 3 sounds you hear.\n"
                "• **Posture:** Gently roll your shoulders back and unclench your jaw.\n\n"
            )
        elif emotion in ["happy", "surprise"]:
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

