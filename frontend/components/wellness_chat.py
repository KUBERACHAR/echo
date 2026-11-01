"""
frontend/components/wellness_chat.py
Chat component for Personalized Mental Wellness Assistance.
"""

import streamlit as st
from backend.gemini_service import GeminiWellnessAssistant

# Initial welcome message
WELCOME_MESSAGE = {
    "role": "assistant",
    "content": (
        "**Welcome to MindCare Companion!**\n\n"
        "I am your **Personalized Mental Wellness Assistant**. "
        "I can help you process your emotions, practice relaxing breathing exercises, relieve workday stress, "
        "and maintain a healthy, balanced state of mind.\n\n"
        "*Tip: As you use the webcam detector, I automatically adapt my guidance to your detected emotion and stress level.*"
    )
}

# Quick action prompt presets
QUICK_PROMPTS = [
    ("🌬️ Calming Breath", "Can you guide me through a 2-minute calming breathing exercise to reset my focus?"),
    ("🧘 Relieve My Stress", "Based on my current state, what are 3 quick techniques I can do right now to relieve stress?"),
    ("💭 Explore My Emotion", "Help me reflect on what my currently detected emotion and stress might be telling me."),
    ("🌱 Positive Affirmation", "Could you share an uplifting, grounding affirmation and reflection for today?"),
    ("☕ Workday Reset", "I've been working at my desk for a while. What's a quick physical and mental stretch routine?"),
]

def init_chat_session():
    """Ensure session state variables for chat are initialized."""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [WELCOME_MESSAGE]
    if "use_emotion_context" not in st.session_state:
        st.session_state.use_emotion_context = True

def render_wellness_chat(gemini_service: GeminiWellnessAssistant):
    """
    Renders the full interactive mental wellness chatbot UI.
    """
    init_chat_session()

    # --- Header & Context Banner ---
    st.markdown("### MindCare AI - Personalized Mental Wellness Companion")

    # Current telemetry context
    curr_emotion = st.session_state.get("current_emotion", "None")
    curr_stress = st.session_state.get("current_stress", "Not Detected")
    curr_confidence = st.session_state.get("current_confidence", 0)

    # Context Card
    with st.container():
        col_ctx1, col_ctx2 = st.columns([3, 1])
        with col_ctx1:
            if curr_emotion and curr_emotion != "None":
                st.info(
                    f"🎯 **Active Emotional Context:** Detected Emotion: **{curr_emotion.capitalize()}** | "
                    f"Stress Level: **{curr_stress}** | Confidence: **{curr_confidence}%**"
                )
            else:
                st.markdown(
                    "<div style='background: #F0F4F8; padding: 0.6rem 1rem; border-radius: 8px; color: #486581; font-size: 0.9rem;'>"
                    "ℹ️ <em>Webcam detection not active or no face detected yet. You can chat freely or start detection on the monitor tab.</em>"
                    "</div>",
                    unsafe_allow_html=True
                )
        with col_ctx2:
            st.session_state.use_emotion_context = st.checkbox(
                "Sync emotion data",
                value=st.session_state.use_emotion_context,
                help="When enabled, your latest detected emotion and stress score are used by Chatbot to tailor answers."
            )

    # --- Quick Action Prompt Chips ---
    st.markdown("##### ⚡ Quick Wellness Starters")
    chip_cols = st.columns(len(QUICK_PROMPTS))
    selected_quick_prompt = None
    for idx, (label, prompt_text) in enumerate(QUICK_PROMPTS):
        with chip_cols[idx]:
            if st.button(label, key=f"quick_prompt_{idx}", use_container_width=True):
                selected_quick_prompt = prompt_text

    st.markdown("---")

    # --- Chat Messages Container ---
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            avatar = "🌿" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    # --- Determine user input (from chat_input or quick chip) ---
    chat_input_val = st.chat_input("Share what's on your mind, or ask for wellness advice...")
    user_prompt = selected_quick_prompt or chat_input_val

    if user_prompt:
        # Append user message
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_prompt)

        # Build emotion context if enabled
        emotion_ctx = None
        if st.session_state.use_emotion_context and curr_emotion and curr_emotion != "None":
            emotion_ctx = {
                "emotion": curr_emotion,
                "stress": curr_stress,
                "confidence": curr_confidence
            }

        # Generate response from Gemini
        with st.chat_message("assistant", avatar="🌿"):
            with st.spinner("MindCare is reflecting on your message..."):
                response_text = gemini_service.generate_wellness_response(
                    user_message=user_prompt,
                    chat_history=st.session_state.chat_messages[:-1],  # exclude just-added message
                    emotion_context=emotion_ctx
                )
                st.markdown(response_text)

        # Append assistant message
        st.session_state.chat_messages.append({"role": "assistant", "content": response_text})

    # --- Utility Bar (Clear Chat) ---
    st.markdown("<br>", unsafe_allow_html=True)
    util_col1, _ = st.columns([1, 4])
    with util_col1:
        if st.button("🗑️ Clear Chat", key="clear_chat_btn", use_container_width=True):
            st.session_state.chat_messages = [WELCOME_MESSAGE]
            st.rerun()

