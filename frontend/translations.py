"""
frontend/translations.py
Multi-language translation dictionaries and helper functions for MindCare AI.
Supported Languages: English (default), Kannada, Hindi, Telugu.
"""

from typing import Dict, List, Tuple

LANGUAGES: List[str] = ["English", "Kannada", "Hindi", "Telugu"]

LANGUAGE_DISPLAY_NAMES: Dict[str, str] = {
    "English": "English",
    "Kannada": "ಕನ್ನಡ (Kannada)",
    "Hindi": "हिन्दी (Hindi)",
    "Telugu": "తెలుగు (Telugu)"
}

TRANSLATIONS: Dict[str, Dict[str, any]] = {
    "English": {
        "header_subtitle": "Real-Time Facial Mood & Stress Detection • Personalized Mental Wellness Chatbot",
        "lang_selector_heading": "🌐 Select Language",
        "tab_monitor": "📹 Live Mood & Stress Tracker",
        "tab_chat": "💬 MindCare AI Wellness Chatbot",
        "live_webcam_feed": "📹 Live Webcam Feed",
        "start_detection": "▶ Start Detection",
        "stop_detection": "⏹ Stop Detection",
        "status_active": "🎥 Camera active. Real-time facial analysis in progress...",
        "status_ended": "✅ Detection session ended. State preserved.",
        "camera_error": "❌ Could not access webcam. Please check your camera permissions and ensure no other application is using it.",
        "frame_warning": "⚠️ Failed to capture video frame.",
        "realtime_telemetry": "📊 Real-Time Telemetry",
        "detected_emotion": "Detected Emotion",
        "stress_level": "Stress Level",
        "confidence_level": "Confidence Level",
        "waiting": "Waiting...",
        "chart_title": "Emotion Probability Breakdown",
        "chart_xaxis": "Probability (%)",
        "emotions": {
            "angry": "Angry",
            "disgust": "Disgust",
            "fear": "Fear",
            "happy": "Happy",
            "neutral": "Neutral",
            "sad": "Sad",
            "surprise": "Surprise"
        },
        "stress_levels": {
            "Low": "Low",
            "Medium": "Medium",
            "High": "High",
            "Not Detected": "Not Detected"
        },
        "sidebar_companion": "MindCare AI Companion",
        "assistant_active": "🟢 AI Assistant Active",
        "assistant_ready": "🟡 AI Assistant Ready",
        "offline_wellness_mode": "Offline wellness mode active",
        "assistant_settings": "⚙️ Assistant Settings",
        "creativity_label": "Creativity / Warmth",
        "creativity_help": "Higher values make responses more conversational and warm.",
        "test_connection_btn": "🧪 Test AI Connection",
        "pinging_api": "Pinging Gemini API...",
        "stress_categories_title": "🎯 Stress Categories",
        "stress_categories_bullets": """- 🟢 **Low:** Calm, balanced or joyful state\n- 🟡 **Medium:** Moderate strain or fatigue detected\n- 🔴 **High:** Heightened stress, tension, or distress""",
        "sidebar_caption": "MindCare AI • Personalized Mental Wellness",
        "chat_header": "MindCare AI - Personalized Mental Wellness Companion",
        "active_context_format": "🎯 **Active Emotional Context:** Detected Emotion: **{emotion}** | Stress Level: **{stress}** | Confidence: **{conf}%**",
        "no_face_notice": "<div style='background: #F0F4F8; padding: 0.6rem 1rem; border-radius: 8px; color: #486581; font-size: 0.9rem;'>ℹ️ <em>Webcam detection not active or no face detected yet. You can chat freely or start detection on the monitor tab.</em></div>",
        "sync_emotion": "Sync emotion data",
        "sync_emotion_help": "When enabled, your latest detected emotion and stress score are used by Chatbot to tailor answers.",
        "quick_starters_title": "##### ⚡ Quick Wellness Starters",
        "quick_prompts": [
            ("🌬️ Calming Breath", "Can you guide me through a 2-minute calming breathing exercise to reset my focus?"),
            ("🧘 Relieve My Stress", "Based on my current state, what are 3 quick techniques I can do right now to relieve stress?"),
            ("💭 Explore My Emotion", "Help me reflect on what my currently detected emotion and stress might be telling me."),
            ("🌱 Positive Affirmation", "Could you share an uplifting, grounding affirmation and reflection for today?"),
            ("☕ Workday Reset", "I've been working at my desk for a while. What's a quick physical and mental stretch routine?"),
        ],
        "chat_input_placeholder": "Share what's on your mind, or ask for wellness advice...",
        "spinner_text": "MindCare is reflecting on your message...",
        "clear_chat": "🗑️ Clear Chat",
        "tts_listen": "Listen to response",
        "tts_stop": "Stop",
        "tts_tooltip": "Listen to freshly generated response",
        "welcome_message": (
            "**Welcome to MindCare Companion!**\n\n"
            "I am your **Personalized Mental Wellness Assistant**. "
            "I can help you process your emotions, practice relaxing breathing exercises, relieve workday stress, "
            "and maintain a healthy, balanced state of mind.\n\n"
            "*Tip: As you use the webcam detector, I automatically adapt my guidance to your detected emotion and stress level.*"
        ),
    },
    "Kannada": {
        "header_subtitle": "ನೈಜ-ಸಮಯದ ಮುಖದ ಭಾವನೆ ಮತ್ತು ಒತ್ತಡ ಪತ್ತೆ • ವೈಯಕ್ತೀಕರಿಸಿದ ಮಾನಸಿಕ ಕ್ಷೇಮ ಚಾಟ್‌ಬಾಟ್",
        "lang_selector_heading": "🌐 ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "tab_monitor": "📹 ನೇರ ಭಾವನೆ ಮತ್ತು ಒತ್ತಡ ಟ್ರ್ಯಾಕರ್",
        "tab_chat": "💬 ಮೈಂಡ್‌ಕೇರ್ AI ಕ್ಷೇಮ ಚಾಟ್‌ಬಾಟ್",
        "live_webcam_feed": "📹 ನೇರ ವೆಬ್‌ಕ್ಯಾಮ್ ಫೀಡ್",
        "start_detection": "▶ ಪತ್ತೆ ಪ್ರಾರಂಭಿಸಿ",
        "stop_detection": "⏹ ಪತ್ತೆ ನಿಲ್ಲಿಸಿ",
        "status_active": "🎥 ಕ್ಯಾಮೆರಾ ಸಕ್ರಿಯವಾಗಿದೆ. ನೈಜ-ಸಮಯದ ಮುಖದ ವಿಶ್ಲೇಷಣೆ ಪ್ರಗತಿಯಲ್ಲಿದೆ...",
        "status_ended": "✅ ಪತ್ತೆ ಅವಧಿ ಮುಕ್ತಾಯಗೊಂಡಿದೆ. ಸ್ಥಿತಿ ಸಂರಕ್ಷಿಸಲಾಗಿದೆ.",
        "camera_error": "❌ ವೆಬ್‌ಕ್ಯಾಮ್ ಪ್ರವೇಶಿಸಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ. ದಯವಿಟ್ಟು ಕ್ಯಾಮೆರಾ ಅನುಮತಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "frame_warning": "⚠️ ವೀಡಿಯೊ ಫ್ರೇಮ್ ಸೆರೆಹಿಡಿಯಲು ವಿಫಲವಾಗಿದೆ.",
        "realtime_telemetry": "📊 ನೈಜ-ಸಮಯದ ಮಾಹಿತಿ",
        "detected_emotion": "ಪತ್ತೆಯಾದ ಭಾವನೆ",
        "stress_level": "ಒತ್ತಡದ ಮಟ್ಟ",
        "confidence_level": "ವಿಶ್ವಾಸಾರ್ಹತೆ ಮಟ್ಟ",
        "waiting": "ನಿರೀಕ್ಷಿಸಲಾಗುತ್ತಿದೆ...",
        "chart_title": "ಭಾವನೆ ಸಂಭವನೀಯತೆಯ ವಿಶ್ಲೇಷಣೆ",
        "chart_xaxis": "ಸಂಭವನೀಯತೆ (%)",
        "emotions": {
            "angry": "ಕೋಪ",
            "disgust": "ಅಸಹ್ಯ",
            "fear": "ಭಯ",
            "happy": "ಸಂತೋಷ",
            "neutral": "ತಟಸ್ಥ",
            "sad": "ದುಃಖ",
            "surprise": "ಆಶ್ಚರ್ಯ"
        },
        "stress_levels": {
            "Low": "ಕಡಿಮೆ",
            "Medium": "ಮಧ್ಯಮ",
            "High": "ಹೆಚ್ಚು",
            "Not Detected": "ಪತ್ತೆಯಾಗಿಲ್ಲ"
        },
        "sidebar_companion": "ಮೈಂಡ್‌ಕೇರ್ AI ಒಡನಾಡಿ",
        "assistant_active": "🟢 AI ಸಹಾಯಕ ಸಕ್ರಿಯವಾಗಿದೆ",
        "assistant_ready": "🟡 AI ಸಹಾಯಕ ಸಿದ್ಧವಾಗಿದೆ",
        "offline_wellness_mode": "ಆಫ್‌ಲೈನ್ ಕ್ಷೇಮ ಮೋಡ್ ಸಕ್ರಿಯವಾಗಿದೆ",
        "assistant_settings": "⚙️ ಸಹಾಯಕ ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
        "creativity_label": "ಸೃಜನಶೀಲತೆ / ಆತ್ಮೀಯತೆ",
        "creativity_help": "ಹೆಚ್ಚಿನ ಮೌಲ್ಯಗಳು ಉತ್ತರಗಳನ್ನು ಹೆಚ್ಚು ಸಂಭಾಷಣಾತ್ಮಕ ಹಾಗೂ ಸಮಾಧಾನಕರವಾಗಿಸುತ್ತವೆ.",
        "test_connection_btn": "🧪 AI ಸಂಪರ್ಕ ಪರೀಕ್ಷಿಸಿ",
        "pinging_api": "Gemini API ಸಂಪರ್ಕ ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",
        "stress_categories_title": "🎯 ಒತ್ತಡದ ವರ್ಗಗಳು",
        "stress_categories_bullets": """- 🟢 **ಕಡಿಮೆ:** ಶಾಂತ, ಸಮತೋಲಿತ ಅಥವಾ ಸಂತೋಷದ ಸ್ಥಿತಿ\n- 🟡 **ಮಧ್ಯಮ:** ಮಧ್ಯಮ ಒತ್ತಡ ಅಥವಾ ಆಯಾಸ ಪತ್ತೆಯಾಗಿದೆ\n- 🔴 **ಹೆಚ್ಚು:** ತೀವ್ರ ಒತ್ತಡ, ಆತಂಕ ಅಥವಾ ಸಂಕಟ""",
        "sidebar_caption": "ಮೈಂಡ್‌ಕೇರ್ AI • ವೈಯಕ್ತೀಕರಿಸಿದ ಮಾನಸಿಕ ಕ್ಷೇಮ",
        "chat_header": "ಮೈಂಡ್‌ಕೇರ್ AI - ವೈಯಕ್ತೀಕರಿಸಿದ ಮಾನಸಿಕ ಕ್ಷೇಮ ಒಡನಾಡಿ",
        "active_context_format": "🎯 **ಸಕ್ರಿಯ ಭಾವನಾತ್ಮಕ ಸಂದರ್ಭ:** ಪತ್ತೆಯಾದ ಭಾವನೆ: **{emotion}** | ಒತ್ತಡ ಮಟ್ಟ: **{stress}** | ವಿಶ್ವಾಸಾರ್ಹತೆ: **{conf}%**",
        "no_face_notice": "<div style='background: #F0F4F8; padding: 0.6rem 1rem; border-radius: 8px; color: #486581; font-size: 0.9rem;'>ℹ️ <em>ವೆಬ್‌ಕ್ಯಾಮ್ ಪತ್ತೆ ಸಕ್ರಿಯವಾಗಿಲ್ಲ ಅಥವಾ ಇನ್ನೂ ಮುಖ ಪತ್ತೆಯಾಗಿಲ್ಲ. ನೀವು ಮುಕ್ತವಾಗಿ ಚಾಟ್ ಮಾಡಬಹುದು ಅಥವಾ ಮಾನಿಟರ್ ಟ್ಯಾಬ್‌ನಲ್ಲಿ ಪತ್ತೆ ಪ್ರಾರಂಭಿಸಬಹುದು.</em></div>",
        "sync_emotion": "ಭಾವನೆ ಮಾಹಿತಿಯನ್ನು ಸಿಂಕ್ ಮಾಡಿ",
        "sync_emotion_help": "ಸಕ್ರಿಯಗೊಳಿಸಿದಾಗ, ನಿಮ್ಮ ಇತ್ತೀಚಿನ ಭಾವನೆ ಮತ್ತು ಒತ್ತಡದ ಸ್ಕೋರ್ ಅನ್ನು ಚಾಟ್‌ಬಾಟ್ ಉತ್ತಮ ಉತ್ತರ ನೀಡಲು ಬಳಸುತ್ತದೆ.",
        "quick_starters_title": "##### ⚡ ತ್ವರಿತ ಕ್ಷೇಮ ಆರಂಭಿಕಗಳು",
        "quick_prompts": [
            ("🌬️ ಶಾಂತಗೊಳಿಸುವ ಉಸಿರಾಟ", "ನನ್ನ ಗಮನವನ್ನು ಮರುಹೊಂದಿಸಲು 2 ನಿಮಿಷಗಳ ಶಾಂತಗೊಳಿಸುವ ಉಸಿರಾಟದ ವ್ಯಾಯಾಮವನ್ನು ಮಾರ್ಗದರ್ಶನ ಮಾಡಬಲ್ಲಿರಾ?"),
            ("🧘 ಒತ್ತಡ ನಿವಾರಿಸಿ", "ನನ್ನ ಪ್ರಸ್ತುತ ಸ್ಥಿತಿಯ ಆಧಾರದ ಮೇಲೆ, ಒತ್ತಡವನ್ನು ಕಡಿಮೆ ಮಾಡಲು ನಾನು ಈಗಲೇ ಮಾಡಬಹುದಾದ 3 ತ್ವರಿತ ವಿಧಾನಗಳು ಯಾವುವು?"),
            ("💭 ನನ್ನ ಭಾವನೆ ಅನ್ವೇಷಿಸಿ", "ಪ್ರಸ್ತುತ ಪತ್ತೆಯಾದ ನನ್ನ ಭಾವನೆ ಮತ್ತು ಒತ್ತಡ ಏನು ತಿಳಿಸುತ್ತಿರಬಹುದು ಎಂದು ಪ್ರತಿಬಿಂಬಿಸಲು ನನಗೆ ಸಹಾಯ ಮಾಡಿ."),
            ("🌱 ಸಕಾರಾತ್ಮಕ ದೃಢೀಕರಣ", "ಇಂದಿನ ದಿನಕ್ಕಾಗಿ ಒಂದು ಸ್ಪೂರ್ತಿದಾಯಕ, ಸಕಾರಾತ್ಮಕ ದೃಢೀಕರಣ ಮತ್ತು ಚಿಂತನೆಯನ್ನು ಹಂಚಿಕೊಳ್ಳಿ."),
            ("☕ ಕೆಲಸದ ನಡುವೆ ವಿರಾಮ", "ನಾನು ಡೆಸ್ಕ್‌ನಲ್ಲಿ ಕೆಲಸ ಮಾಡುತ್ತಿದ್ದೇನೆ. ತ್ವರಿತ ದೈಹಿಕ ಮತ್ತು ಮಾನಸಿಕ ವಿಶ್ರಾಂತಿ ದಿನಚರಿ ಏನು?"),
        ],
        "chat_input_placeholder": "ನಿಮ್ಮ ಮನಸ್ಸಿನಲ್ಲಿರುವುದನ್ನು ಹಂಚಿಕೊಳ್ಳಿ, ಅಥವಾ ಕ್ಷೇಮ ಸಲಹೆ ಕೇಳಿ...",
        "spinner_text": "ಮೈಂಡ್‌ಕೇರ್ ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಪರಿಶೀಲಿಸುತ್ತಿದೆ...",
        "clear_chat": "🗑️ ಚಾಟ್ ಅಳಿಸಿ",
        "tts_listen": "ಉತ್ತರವನ್ನು ಆಲಿಸಿ",
        "tts_stop": "ನಿಲ್ಲಿಸಿ",
        "tts_tooltip": "ಹೊಸದಾಗಿ ರಚಿಸಲಾದ ಉತ್ತರವನ್ನು ಆಲಿಸಿ",
        "welcome_message": (
            "**ಮೈಂಡ್‌ಕೇರ್ ಕಂಪ್ಯಾನಿಯನ್‌ಗೆ ಸುಸ್ವಾಗತ!**\n\n"
            "ನಾನು ನಿಮ್ಮ **ವೈಯಕ್ತಿಕ ಮಾನಸಿಕ ಕ್ಷೇಮ ಸಹಾಯಕ**. "
            "ನಿಮ್ಮ ಭಾವನೆಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು, ವಿಶ್ರಾಂತಿ ನೀಡುವ ಉಸಿರಾಟದ ವ್ಯಾಯಾಮಗಳನ್ನು ಅಭ್ಯಾಸ ಮಾಡಲು, ಕೆಲಸದ ಒತ್ತಡ ನಿವಾರಿಸಲು "
            "ಮತ್ತು ಸಮತೋಲಿತ ಮನಸ್ಥಿತಿಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಲು ನಾನು ಸಹಾಯ ಮಾಡುತ್ತೇನೆ.\n\n"
            "*ಸಲಹೆ: ನೀವು ವೆಬ್‌ಕ್ಯಾಮ್ ಡಿಟೆಕ್ಟರ್ ಬಳಸಿದಂತೆ, ಪತ್ತೆಯಾದ ಭಾವನೆ ಮತ್ತು ಒತ್ತಡದ ಮಟ್ಟಕ್ಕೆ ತಕ್ಕಂತೆ ನನ್ನ ಮಾರ್ಗದರ್ಶನವನ್ನು ಹೊಂದಿಸಿಕೊಳ್ಳುತ್ತೇನೆ.*"
        ),
    },
    "Hindi": {
        "header_subtitle": "रीयल-टाइम फेशियल मूड और तनाव पहचान • व्यक्तिगत मानसिक स्वास्थ्य चैटबॉट",
        "lang_selector_heading": "🌐 भाषा चुनें",
        "tab_monitor": "📹 लाइव मूड और तनाव ट्रैकर",
        "tab_chat": "💬 माइंडकेयर AI वेलनेस चैटबॉट",
        "live_webcam_feed": "📹 लाइव वेबकैम फीड",
        "start_detection": "▶ डिटेक्शन शुरू करें",
        "stop_detection": "⏹ डिटेक्शन रोकें",
        "status_active": "🎥 कैमरा सक्रिय है। रीयल-टाइम चेहरे का विश्लेषण जारी है...",
        "status_ended": "✅ डिटेक्शन सत्र समाप्त हुआ। डेटा सुरक्षित है।",
        "camera_error": "❌ वेबकैम तक नहीं पहुँच सके। कृपया कैमरा अनुमतियों की जांच करें।",
        "frame_warning": "⚠️ वीडियो फ्रेम कैप्चर करने में विफल।",
        "realtime_telemetry": "📊 रीयल-टाइम टेलीमेट्री",
        "detected_emotion": "पहचानी गई भावना",
        "stress_level": "तनाव का स्तर",
        "confidence_level": "सटीकता / विश्वास स्तर",
        "waiting": "प्रतीक्षारत...",
        "chart_title": "भावना संभावना विश्लेषण",
        "chart_xaxis": "संभावना (%)",
        "emotions": {
            "angry": "क्रोध",
            "disgust": "घृणा",
            "fear": "डर",
            "happy": "प्रसन्न",
            "neutral": "तटस्थ",
            "sad": "उदास",
            "surprise": "आश्चर्य"
        },
        "stress_levels": {
            "Low": "निम्न",
            "Medium": "मध्यम",
            "High": "उच्च",
            "Not Detected": "पहचाना नहीं गया"
        },
        "sidebar_companion": "माइंडकेयर AI साथी",
        "assistant_active": "🟢 AI सहायक सक्रिय है",
        "assistant_ready": "🟡 AI सहायक तैयार है",
        "offline_wellness_mode": "ऑफ़लाइन वेलनेस मोड सक्रिय है",
        "assistant_settings": "⚙️ सहायक सेटिंग्स",
        "creativity_label": "रचनात्मकता / आत्मीयता",
        "creativity_help": "उच्च मान उत्तरों को अधिक संवादात्मक और आत्मीय बनाते हैं।",
        "test_connection_btn": "🧪 AI कनेक्शन का परीक्षण करें",
        "pinging_api": "Gemini API की जांच की जा रही है...",
        "stress_categories_title": "🎯 तनाव की श्रेणियाँ",
        "stress_categories_bullets": """- 🟢 **निम्न:** शांत, संतुलित या प्रसन्न स्थिति\n- 🟡 **मध्यम:** सामान्य तनाव या थकान पहचानी गई\n- 🔴 **उच्च:** अत्यधिक तनाव, खिंचाव या चिंता""",
        "sidebar_caption": "माइंडकेयर AI • व्यक्तिगत मानसिक स्वास्थ्य",
        "chat_header": "माइंडकेयर AI - व्यक्तिगत मानसिक स्वास्थ्य साथी",
        "active_context_format": "🎯 **सक्रिय भावनात्मक संदर्भ:** पहचानी गई भावना: **{emotion}** | तनाव स्तर: **{stress}** | सटीकता: **{conf}%**",
        "no_face_notice": "<div style='background: #F0F4F8; padding: 0.6rem 1rem; border-radius: 8px; color: #486581; font-size: 0.9rem;'>ℹ️ <em>वेबकैम डिटेक्शन सक्रिय नहीं है या अभी तक कोई चेहरा नहीं दिखा है। आप स्वतंत्र रूप से चैट कर सकते हैं या ट्रैकर शुरू कर सकते हैं।</em></div>",
        "sync_emotion": "भावना डेटा सिंक करें",
        "sync_emotion_help": "सक्रिय होने पर, आपकी नवीनतम पहचानी गई भावना और तनाव स्कोर का उपयोग चैटबॉट द्वारा उत्तरों को अनुकूलित करने के लिए किया जाता है।",
        "quick_starters_title": "##### ⚡ त्वरित वेलनेस विकल्प",
        "quick_prompts": [
            ("🌬️ शांत श्वास", "क्या आप मेरा ध्यान केंद्रित करने के लिए 2 मिनट के शांत श्वास व्यायाम में मेरा मार्गदर्शन कर सकते हैं?"),
            ("🧘 तनाव कम करें", "मेरी वर्तमान स्थिति के आधार पर, तनाव दूर करने के लिए मैं अभी कौन सी 3 त्वरित तकनीकें अपना सकता हूँ?"),
            ("💭 मेरी भावना समझें", "वर्तमान में पहचानी गई मेरी भावना और तनाव क्या संकेत दे रहे हैं, इसे समझने में मेरी मदद करें।"),
            ("🌱 सकारात्मक विचार", "क्या आप आज के लिए एक उत्साहजनक, सकारात्मक विचार और प्रेरणा साझा कर सकते हैं?"),
            ("☕ कार्यदिवस रीसेट", "मैं काफी देर से डेस्क पर काम कर रहा हूँ। एक त्वरित शारीरिक और मानसिक स्ट्रेच रूटीन क्या है?"),
        ],
        "chat_input_placeholder": "अपने मन की बात साझा करें, या स्वास्थ्य संबंधी सलाह लें...",
        "spinner_text": "माइंडकेयर आपके संदेश पर विचार कर रहा है...",
        "clear_chat": "🗑️ चैट साफ़ करें",
        "tts_listen": "उत्तर सुनें",
        "tts_stop": "रोकें",
        "tts_tooltip": "नए उत्पन्न उत्तर को सुनें",
        "welcome_message": (
            "**माइंडकेयर कंपैनियन में आपका स्वागत है!**\n\n"
            "मैं आपका **व्यक्तिगत मानसिक स्वास्थ्य सहायक** हूँ। "
            "मैं आपकी भावनाओं को समझने, तनाव दूर करने वाले श्वास व्यायाम करने, काम के तनाव को कम करने "
            "और एक स्वस्थ, संतुलित मानसिक स्थिति बनाए रखने में मदद कर सकता हूँ।\n\n"
            "*सुझाव: जब आप वेबकैम डिटेक्टर का उपयोग करते हैं, तो मैं आपकी पहचानी गई भावना और तनाव स्तर के अनुसार मार्गदर्शन को अनुकूलित करूँगा।*"
        ),
    },
    "Telugu": {
        "header_subtitle": "నిజ-సమయ ముఖ భావోద్వేగం & ఒత్తిడి గుర్తింపు • వ్యక్తిగతీకరించిన మానసిక శ్రేయస్సు చాట్‌బాట్",
        "lang_selector_heading": "🌐 భాషను ఎంచుకోండి",
        "tab_monitor": "📹 లైవ్ మూడ్ & ఒత్తిడి ట్రాకర్",
        "tab_chat": "💬 మైండ్‌కేర్ AI శ్రేయస్సు చాట్‌బాట్",
        "live_webcam_feed": "📹 లైవ్ వెబ్‌క్యామ్ ఫీడ్",
        "start_detection": "▶ గుర్తింపు ప్రారంభించండి",
        "stop_detection": "⏹ గుర్తింపు ఆపండి",
        "status_active": "🎥 కెమెరా సక్రియంగా ఉంది. నిజ-సమయ ముఖ విశ్లేషణ జరుగుతోంది...",
        "status_ended": "✅ గుర్తింపు ముగిసింది. స్థితి భద్రపరచబడింది.",
        "camera_error": "❌ వెబ్‌క్యామ్‌ని యాక్సెస్ చేయడం సాధ్యపడలేదు. దయచేసి కెమెరా అనుమతులను తనిఖీ చేయండి.",
        "frame_warning": "⚠️ వీడియో ఫ్రేమ్‌ను క్యాప్చర్ చేయడంలో విఫలమైంది.",
        "realtime_telemetry": "📊 నిజ-సమయ టెలిమెట్రీ",
        "detected_emotion": "గుర్తించిన భావోద్వేగం",
        "stress_level": "ఒత్తిడి స్థాయి",
        "confidence_level": "విశ్వసనీయత స్థాయి",
        "waiting": "వేచి చూస్తోంది...",
        "chart_title": "భావోద్వేగ సంభావ్యత విశ్లేషణ",
        "chart_xaxis": "సంభావ్యత (%)",
        "emotions": {
            "angry": "కోపం",
            "disgust": "అసహ్యం",
            "fear": "భయం",
            "happy": "ఆనందం",
            "neutral": "తటస్థం",
            "sad": "విచారం",
            "surprise": "ఆశ్చర్యం"
        },
        "stress_levels": {
            "Low": "తక్కువ",
            "Medium": "మధ్యస్థం",
            "High": "ఎక్కువ",
            "Not Detected": "గుర్తించబడలేదు"
        },
        "sidebar_companion": "మైండ్‌కేర్ AI సహచరుడు",
        "assistant_active": "🟢 AI సహాయకుడు సక్రియంగా ఉన్నారు",
        "assistant_ready": "🟡 AI సహాయకుడు సిద్ధంగా ఉన్నారు",
        "offline_wellness_mode": "ఆఫ్‌లైన్ శ్రేయస్సు మోడ్ సక్రియంగా ఉంది",
        "assistant_settings": "⚙️ సహాయక సెట్టింగ్‌లు",
        "creativity_label": "సృజనాత్మకత / ఆత్మీయత",
        "creativity_help": "అధిక విలువలు ప్రతిస్పందనలను మరింత స్నేహపూర్వకంగా మరియు ఆత్మీయంగా చేస్తాయి.",
        "test_connection_btn": "🧪 AI కనెక్షన్‌ని పరీక్షించండి",
        "pinging_api": "Gemini API తనిఖీ చేయబడుతోంది...",
        "stress_categories_title": "🎯 ఒత్తిడి వర్గాలు",
        "stress_categories_bullets": """- 🟢 **తక్కువ:** ప్రశాంత, సమతుల్య లేదా ఆనందకరమైన స్థితి\n- 🟡 **మధ్యస్థం:** మోస్తరు ఒత్తిడి లేదా అలసట గుర్తించబడింది\n- 🔴 **ఎక్కువ:** తీవ్రమైన ఒత్తిడి, ఆందోళన లేదా వేదన""",
        "sidebar_caption": "మైండ్‌కేర్ AI • వ్యక్తిగతీకరించిన మానసిక శ్రేయస్సు",
        "chat_header": "మైండ్‌కేర్ AI - వ్యక్తిగతీకరించిన మానసిక శ్రేయస్సు సహచరుడు",
        "active_context_format": "🎯 **సక్రియ భావోద్వేగ సందర్భం:** గుర్తించిన భావోద్వేగం: **{emotion}** | ఒత్తిడి స్థాయి: **{stress}** | విశ్వసనీయత: **{conf}%**",
        "no_face_notice": "<div style='background: #F0F4F8; padding: 0.6rem 1rem; border-radius: 8px; color: #486581; font-size: 0.9rem;'>ℹ️ <em>వెబ్‌క్యామ్ గుర్తింపు సక్రియంగా లేదు లేదా ఇంకా ముఖం గుర్తించబడలేదు. మీరు స్వేచ్ఛగా చాట్ చేయవచ్చు లేదా ట్రాకర్‌లో ప్రారంభించవచ్చు.</em></div>",
        "sync_emotion": "భావోద్వేగ సమాచారాన్ని సమకాలీకరించండి",
        "sync_emotion_help": "ఎనేబుల్ చేసినప్పుడు, మీ తాజా భావోద్వేగం మరియు ఒత్తిడి స్కోర్‌ను సమాధానాలు మెరుగుపరచడానికి చాట్‌బాట్ ఉపయోగిస్తుంది.",
        "quick_starters_title": "##### ⚡ శీఘ్ర శ్రేయస్సు ప్రారంభాలు",
        "quick_prompts": [
            ("🌬️ ప్రశాంత శ్వాస", "నా ఏకాగ్రతను తిరిగి పొందడానికి 2 నిమిషాల ప్రశాంత శ్వాస వ్యాయామంలో నాకు మార్గదర్శకత్వం చేయగలరా?"),
            ("🧘 ఒత్తిడి నివారణ", "నా ప్రస్తుత స్థితి ఆధారంగా, ఒత్తిడిని తగ్గించుకోవడానికి నేను ఇప్పుడే చేయగలిగే 3 శీఘ్ర పద్ధతులు ఏమిటి?"),
            ("💭 నా భావోద్వేగాన్ని అన్వేషించండి", "ప్రస్తుతం గుర్తించబడిన నా భావోద్వేగం మరియు ఒత్తిడి ఏమి చెబుతున్నాయో అర్థం చేసుకోవడంలో నాకు సహాయపడండి."),
            ("🌱 సానుకూల ధృవీకరణ", "ఈ రోజు కోసం ఉత్తేజకరమైన, సానుకూల ధృవీకరణ మరియు ఆలోచనను పంచుకోగలరా?"),
            ("☕ పని విరామం", "నేను చాలా సేపటి నుండి డెస్క్ వద్ద పనిచేస్తున్నాను. శీఘ్ర శారీరక మరియు మానసిక విశ్రాంతి పద్ధతి ఏమిటి?"),
        ],
        "chat_input_placeholder": "మీ మనస్సులోని ఆలోచనలను పంచుకోండి, లేదా శ్రేయస్సు సలహా అడగండి...",
        "spinner_text": "మైండ్‌కేర్ మీ సందేశాన్ని పరిశీలిస్తోంది...",
        "clear_chat": "🗑️ చాట్ క్లియర్ చేయండి",
        "tts_listen": "సమాధానం వినండి",
        "tts_stop": "ఆపండి",
        "tts_tooltip": "కొత్తగా రూపొందించిన సమాధానాన్ని వినండి",
        "welcome_message": (
            "**మైండ్‌కేర్ కంపానియన్‌కి స్వాగతం!**\n\n"
            "నేను మీ **వ్యక్తిగతీకరించిన మానసిక శ్రేయస్సు సహాయకుడిని**. "
            "మీ భావోద్వేగాలను అర్థం చేసుకోవడంలో, విశ్రాంతి శ్వాస వ్యాయామాలను అభ్యసించడంలో, పని ఒత్తిడిని తగ్గించుకోవడంలో "
            "మరియు సమతుల్య మానసిక స్థితిని కాపాడుకోవడంలో నేను మీకు సహాయపడగలను.\n\n"
            "*చిట్కా: మీరు వెబ్‌క్యామ్ డిటెక్టర్‌ని ఉపయోగించినప్పుడు, గుర్తించిన భావోద్వేగం మరియు ఒత్తిడి స్థాయికి అనుగుణంగా నా మార్గదర్శకత్వాన్ని అందిస్తాను.*"
        ),
    }
}

def get_text(key: str, lang: str = "English", default: str = "") -> any:
    """Retrieve translated text string for given key and language."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
    return lang_dict.get(key, TRANSLATIONS["English"].get(key, default))

def get_emotion_label(emotion_key: str, lang: str = "English") -> str:
    """Get translated emotion label."""
    emotions = get_text("emotions", lang, {})
    return emotions.get(emotion_key.lower(), emotion_key.capitalize())

def get_stress_label(stress_key: str, lang: str = "English") -> str:
    """Get translated stress level label."""
    stress_levels = get_text("stress_levels", lang, {})
    return stress_levels.get(stress_key, stress_key)

def get_quick_prompts(lang: str = "English") -> List[Tuple[str, str]]:
    """Get translated quick prompts list."""
    return get_text("quick_prompts", lang, TRANSLATIONS["English"]["quick_prompts"])

def get_welcome_message(lang: str = "English") -> str:
    """Get translated welcome message."""
    return get_text("welcome_message", lang, TRANSLATIONS["English"]["welcome_message"])
