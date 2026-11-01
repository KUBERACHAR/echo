"""
frontend/components/wellness_chat.py
Chat component for Personalized Mental Wellness Assistance.
Supports dynamic multi-language interface and responses (English, Kannada, Hindi, Telugu).
"""

import streamlit as st
from backend.gemini_service import GeminiWellnessAssistant
from frontend.translations import (
    get_text,
    get_emotion_label,
    get_stress_label,
    get_quick_prompts,
    get_welcome_message
)

def init_chat_session(language: str = "English"):
    """Ensure session state variables for chat are initialized with active language."""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": get_welcome_message(language)}
        ]
        st.session_state.chat_language = language

    if "use_emotion_context" not in st.session_state:
        st.session_state.use_emotion_context = True

    # If language has changed and chat only contains the initial greeting, update it
    prev_lang = st.session_state.get("chat_language", "English")
    if prev_lang != language:
        st.session_state.chat_language = language
        if (
            len(st.session_state.chat_messages) == 1
            and st.session_state.chat_messages[0].get("role") == "assistant"
        ):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": get_welcome_message(language)}
            ]

def render_wellness_chat(gemini_service: GeminiWellnessAssistant, language: str = "English"):
    """
    Renders the full interactive mental wellness chatbot UI.
    Dynamically localized to the user-selected language.
    """
    init_chat_session(language)

    # --- Header & Context Banner ---
    st.markdown(f"### {get_text('chat_header', language)}")

    # Current telemetry context
    curr_emotion = st.session_state.get("current_emotion", "None")
    curr_stress = st.session_state.get("current_stress", "Not Detected")
    curr_confidence = st.session_state.get("current_confidence", 0)

    # Context Card
    with st.container():
        col_ctx1, col_ctx2 = st.columns([3, 1])
        with col_ctx1:
            if curr_emotion and curr_emotion != "None":
                localized_emotion = get_emotion_label(curr_emotion, language)
                localized_stress = get_stress_label(curr_stress, language)
                context_msg = get_text("active_context_format", language).format(
                    emotion=localized_emotion,
                    stress=localized_stress,
                    conf=curr_confidence
                )
                st.info(context_msg)
            else:
                st.markdown(get_text("no_face_notice", language), unsafe_allow_html=True)
        with col_ctx2:
            st.session_state.use_emotion_context = st.checkbox(
                get_text("sync_emotion", language),
                value=st.session_state.use_emotion_context,
                help=get_text("sync_emotion_help", language)
            )

    # --- Quick Action Prompt Chips ---
    st.markdown(get_text("quick_starters_title", language))
    quick_prompts = get_quick_prompts(language)
    chip_cols = st.columns(len(quick_prompts))
    selected_quick_prompt = None
    for idx, (label, prompt_text) in enumerate(quick_prompts):
        with chip_cols[idx]:
            if st.button(label, key=f"quick_prompt_{language}_{idx}", use_container_width=True):
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
    chat_input_val = st.chat_input(get_text("chat_input_placeholder", language))
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

        # Generate response from Gemini in the selected language
        with st.chat_message("assistant", avatar="🌿"):
            with st.spinner(get_text("spinner_text", language)):
                response_text = gemini_service.generate_wellness_response(
                    user_message=user_prompt,
                    chat_history=st.session_state.chat_messages[:-1],  # exclude just-added message
                    emotion_context=emotion_ctx,
                    language=language
                )
                st.markdown(response_text)

        # Append assistant message
        st.session_state.chat_messages.append({"role": "assistant", "content": response_text})

    # --- Utility Bar (Clear Chat) ---
    st.markdown("<br>", unsafe_allow_html=True)
    util_col1, _ = st.columns([1, 4])
    with util_col1:
        if st.button(get_text("clear_chat", language), key="clear_chat_btn", use_container_width=True):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": get_welcome_message(language)}
            ]
            st.rerun()
