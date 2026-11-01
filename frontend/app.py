# frontend/app.py
"""
MindCare - Real-Time Facial Emotion & Stress Detection with Mental Wellness Assistant.
Supports dynamic multi-language interface and responses (English, Kannada, Hindi, Telugu).
"""

import os
import sys
import time
import cv2
import numpy as np
import streamlit as st

# Ensure root directory is on Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Optimize TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from tensorflow.keras.models import load_model
from mtcnn import MTCNN

# Internal modules & components
import config
from backend.gemini_service import GeminiWellnessAssistant
from frontend.translations import (
    LANGUAGES,
    LANGUAGE_DISPLAY_NAMES,
    get_text,
    get_emotion_label,
    get_stress_label
)
from frontend.components.emotion_chart import render_emotion_chart
from frontend.components.stress_meter import render_stress_gauge
from frontend.components.live_feed import draw_emotion_overlay
from frontend.components.wellness_chat import render_wellness_chat

DEVELOPER_API_KEY = getattr(config, "GEMINI_API_KEY", "")
DEFAULT_MODEL = getattr(config, "DEFAULT_GEMINI_MODEL", "gemini-3.5-flash-lite")
DEFAULT_TEMP = getattr(config, "DEFAULT_TEMPERATURE", 0.7)

# --- Configuration & Paths ---
MODEL_PATH = os.path.join(BASE_DIR, "models", "emotion_model.h5")
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(BASE_DIR, "frontend", "models", "emotion_model.h5")

EMOTIONS = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

# Hardcoded camera & detection settings
DEFAULT_CAM_INDEX = 0
MIN_FACE_CONF = 0.90

EMOTION_ICONS = {
    "angry": "😠",
    "disgust": "🤢",
    "fear": "😨",
    "happy": "😊",
    "neutral": "😐",
    "sad": "😢",
    "surprise": "😲"
}

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="MindCare - Mood, Stress & Wellness AI",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Wellness Theme) ---
st.markdown("""
<style>
    /* Wellness Palette */
    :root {
        --primary-blue: #4A90E2;
        --soft-green: #7BC96F;
        --calm-teal: #5DADE2;
        --neutral-grey: #F5F7FA;
        --text-dark: #2C3E50;
        --warning-amber: #F39C12;
        --danger-red: #E74C3C;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main-header {
        text-align: center;
        padding: 2rem 2rem 1.6rem 2rem;
        background: linear-gradient(135deg, #4A00E0 0%, #8E2DE2 50%, #5DADE2 100%);
        color: white;
        border-radius: 18px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(110, 72, 170, 0.25);
    }
    
    .main-header h1 {
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 1px 2px 4px rgba(0,0,0,0.25);
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.95;
        font-weight: 300;
    }

    .lang-bar {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    
    .result-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        border: 1px solid #E8ECEF;
    }
    
    .result-card h3 {
        color: #2C3E50;
        margin-top: 0;
        font-size: 1.05rem;
        font-weight: 700;
    }
    
    .emotion-display {
        font-size: 3.8rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .emotion-label {
        font-size: 1.4rem;
        text-align: center;
        font-weight: 700;
        color: #2C3E50;
        text-transform: capitalize;
    }
    
    .stress-indicator {
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .stress-low {
        background: #E8F5E9;
        color: #1B5E20;
        border: 2px solid #7BC96F;
    }
    
    .stress-medium {
        background: #FFF3E0;
        color: #E65100;
        border: 2px solid #F39C12;
    }
    
    .stress-high {
        background: #FFEBEE;
        color: #B71C1C;
        border: 2px solid #E74C3C;
    }
    
    .confidence-bar {
        background: #E0E0E0;
        border-radius: 12px;
        height: 22px;
        overflow: hidden;
        margin: 0.6rem 0;
    }
    
    .confidence-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 12px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "English"  # Default language
if 'show_privacy' not in st.session_state:
    st.session_state.show_privacy = True
if 'detection_active' not in st.session_state:
    st.session_state.detection_active = False
if 'current_emotion' not in st.session_state:
    st.session_state.current_emotion = "None"
if 'current_stress' not in st.session_state:
    st.session_state.current_stress = "Not Detected"
if 'current_confidence' not in st.session_state:
    st.session_state.current_confidence = 0
if 'latest_predictions' not in st.session_state:
    st.session_state.latest_predictions = [0.0] * 7
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = DEVELOPER_API_KEY
if 'gemini_model' not in st.session_state:
    st.session_state.gemini_model = DEFAULT_MODEL
if 'gemini_temp' not in st.session_state:
    st.session_state.gemini_temp = DEFAULT_TEMP

curr_lang = st.session_state.selected_language

# --- Header ---
st.markdown(f"""
<div class="main-header">
    <h1>ECHO</h1>
    <p>{get_text('header_subtitle', curr_lang)}</p>
</div>
""", unsafe_allow_html=True)

# --- Language Selection Bar (Prominent Button Interface) ---
st.markdown(f"""
<div style="font-weight: 700; color: #334155; font-size: 0.95rem; margin-bottom: 0.4rem;">
    {get_text('lang_selector_heading', curr_lang)}:
</div>
""", unsafe_allow_html=True)

lang_cols = st.columns(len(LANGUAGES))
for idx, lang_opt in enumerate(LANGUAGES):
    with lang_cols[idx]:
        is_active = (curr_lang == lang_opt)
        display_label = LANGUAGE_DISPLAY_NAMES.get(lang_opt, lang_opt)
        if st.button(
            display_label,
            key=f"lang_btn_{lang_opt}",
            type="primary" if is_active else "secondary",
            use_container_width=True
        ):
            if st.session_state.selected_language != lang_opt:
                st.session_state.selected_language = lang_opt
                st.rerun()

st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# --- Model Loading (Cached) ---
@st.cache_resource
def load_cached_emotion_model():
    try:
        model = load_model(MODEL_PATH)
        return model, None
    except Exception as e:
        return None, str(e)

@st.cache_resource
def load_cached_face_detector():
    return MTCNN()

# Load models with friendly spinner
with st.spinner("🔄 Initializing emotion detection models..."):
    emotion_model, model_err = load_cached_emotion_model()
    if emotion_model is None:
        st.error(f"❌ **Error loading emotion model from `{MODEL_PATH}`:**\n\n`{model_err}`")
        st.info("💡 Please place `emotion_model.h5` inside the `models/` directory.")
        st.stop()
    face_detector = load_cached_face_detector()

# Stress estimation algorithm
def estimate_stress_from_emotion(emotion, confidence_scores):
    """Estimate stress score (0-100) and category from emotion probabilities."""
    stress_emotions = [0, 2, 5]  # angry (0), fear (2), sad (5)
    raw_stress_score = sum(confidence_scores[i] for i in stress_emotions)
    stress_pct = int(min(max(raw_stress_score * 100, 0), 100))

    if raw_stress_score > 0.45:
        return "High", "stress-high", stress_pct
    elif raw_stress_score > 0.20:
        return "Medium", "stress-medium", stress_pct
    else:
        return "Low", "stress-low", stress_pct

# --- Initialize Gemini Wellness Assistant ---
gemini_assistant = GeminiWellnessAssistant(
    api_key=st.session_state.gemini_api_key,
    model=st.session_state.gemini_model,
    temperature=st.session_state.gemini_temp
)

# --- Sidebar Configuration & Navigation ---
with st.sidebar:
    st.markdown(f"## {get_text('sidebar_companion', curr_lang)}")

    # Synchronized Sidebar Language Selector
    sidebar_lang = st.selectbox(
        get_text('lang_selector_heading', curr_lang),
        options=LANGUAGES,
        index=LANGUAGES.index(curr_lang) if curr_lang in LANGUAGES else 0,
        format_func=lambda l: LANGUAGE_DISPLAY_NAMES.get(l, l),
        key="sidebar_lang_selector"
    )
    if sidebar_lang != curr_lang:
        st.session_state.selected_language = sidebar_lang
        st.rerun()

    # Assistant Status Badge
    if gemini_assistant.is_configured():
        st.markdown(f"""
        <div style="background: #E8F5E9; border-left: 4px solid #2E7D32; padding: 0.65rem 0.85rem; border-radius: 8px; margin-bottom: 0.8rem;">
            <strong style="color: #1B5E20; font-size: 0.95rem;">{get_text('assistant_active', curr_lang)}</strong><br>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: #FFF8E1; border-left: 4px solid #F57F17; padding: 0.65rem 0.85rem; border-radius: 8px; margin-bottom: 0.8rem;">
            <strong style="color: #E65100; font-size: 0.95rem;">{get_text('assistant_ready', curr_lang)}</strong><br>
            <span style="font-size: 0.82rem; color: #5D4037;">{get_text('offline_wellness_mode', curr_lang)}</span>
        </div>
        """, unsafe_allow_html=True)

    with st.expander(get_text('assistant_settings', curr_lang)):
        selected_model = st.selectbox(
            "Gemini Model",
            options=GeminiWellnessAssistant.AVAILABLE_MODELS,
            index=GeminiWellnessAssistant.AVAILABLE_MODELS.index(st.session_state.gemini_model)
            if st.session_state.gemini_model in GeminiWellnessAssistant.AVAILABLE_MODELS else 0
        )
        if selected_model != st.session_state.gemini_model:
            st.session_state.gemini_model = selected_model
            gemini_assistant.set_model(selected_model)

        temp_val = st.slider(
            get_text('creativity_label', curr_lang),
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.gemini_temp,
            step=0.05,
            help=get_text('creativity_help', curr_lang)
        )
        if temp_val != st.session_state.gemini_temp:
            st.session_state.gemini_temp = temp_val
            gemini_assistant.set_temperature(temp_val)

        if st.button(get_text('test_connection_btn', curr_lang), use_container_width=True):
            with st.spinner(get_text('pinging_api', curr_lang)):
                ok, msg = gemini_assistant.test_connection()
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    st.markdown("---")
    st.markdown(f"## {get_text('stress_categories_title', curr_lang)}")
    st.markdown(get_text('stress_categories_bullets', curr_lang))

    st.markdown("---")
    st.markdown(f"**Model:** `{os.path.basename(MODEL_PATH)}`")
    st.caption(get_text('sidebar_caption', curr_lang))

# --- Main Tabs (Dynamically Localized) ---
tab_monitor, tab_chat = st.tabs([
    get_text("tab_monitor", curr_lang),
    get_text("tab_chat", curr_lang)
])

# =========================================================================
# TAB 1: Live Mood & Stress Tracker
# =========================================================================
with tab_monitor:
    col_video, col_metrics = st.columns([3, 2], gap="large")

    with col_video:
        st.markdown(f"### {get_text('live_webcam_feed', curr_lang)}")
        frame_placeholder = st.empty()

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            start_btn = st.button(
                get_text("start_detection", curr_lang),
                type="primary",
                use_container_width=True,
                key="start_det"
            )
        with btn_col2:
            stop_btn = st.button(
                get_text("stop_detection", curr_lang),
                use_container_width=True,
                key="stop_det"
            )

        # Status badge below video
        status_box = st.empty()

    with col_metrics:
        st.markdown(f"### {get_text('realtime_telemetry', curr_lang)}")
        emotion_placeholder = st.empty()
        stress_placeholder = st.empty()
        confidence_placeholder = st.empty()
        chart_placeholder = st.empty()

        # Display initial / current metrics with localization
        curr_icon = EMOTION_ICONS.get(st.session_state.current_emotion, "🤖")
        if st.session_state.current_emotion != "None":
            curr_em_label = get_emotion_label(st.session_state.current_emotion, curr_lang)
        else:
            curr_em_label = get_text("waiting", curr_lang)

        curr_stress_label = get_stress_label(st.session_state.current_stress, curr_lang)

        with emotion_placeholder.container():
            st.markdown(f"""
            <div class="result-card">
                <h3>{get_text('detected_emotion', curr_lang)}</h3>
                <div class="emotion-display">{curr_icon}</div>
                <div class="emotion-label">{curr_em_label}</div>
            </div>
            """, unsafe_allow_html=True)

        with stress_placeholder.container():
            stress_style = "stress-low"
            if st.session_state.current_stress == "High":
                stress_style = "stress-high"
            elif st.session_state.current_stress == "Medium":
                stress_style = "stress-medium"
            st.markdown(f"""
            <div class="result-card">
                <h3>{get_text('stress_level', curr_lang)}</h3>
                <div class="stress-indicator {stress_style}">
                    {curr_stress_label}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with confidence_placeholder.container():
            st.markdown(f"""
            <div class="result-card">
                <h3>{get_text('confidence_level', curr_lang)}</h3>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {st.session_state.current_confidence}%;"></div>
                </div>
                <p style="text-align: center; color: #2C3E50; font-weight: 600; margin: 0;">{st.session_state.current_confidence}%</p>
            </div>
            """, unsafe_allow_html=True)

        # Plotly Emotion Probability Chart with active language
        with chart_placeholder.container():
            fig = render_emotion_chart(EMOTIONS, st.session_state.latest_predictions, language=curr_lang)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Handle button events
    if start_btn:
        st.session_state.detection_active = True
    if stop_btn:
        st.session_state.detection_active = False

    # Detection Loop
    if st.session_state.detection_active:
        cap = cv2.VideoCapture(DEFAULT_CAM_INDEX)
        if not cap.isOpened():
            st.error(get_text("camera_error", curr_lang))
            st.session_state.detection_active = False
        else:
            status_box.info(get_text("status_active", curr_lang))

            while st.session_state.detection_active:
                ret, frame = cap.read()
                if not ret:
                    st.warning(get_text("frame_warning", curr_lang))
                    break

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                try:
                    detections = face_detector.detect_faces(rgb_frame)
                    
                    found_face = False
                    for detection in detections:
                        conf = detection.get('confidence', 0.0)
                        if conf < MIN_FACE_CONF:
                            continue

                        box = detection.get('box', [0, 0, 0, 0])
                        x, y, w, h = box
                        x, y = max(0, x), max(0, y)
                        w, h = max(1, w), max(1, h)

                        face = rgb_frame[y:y+h, x:x+w]
                        if face.size == 0:
                            continue

                        found_face = True
                        face_resized = cv2.resize(face, (96, 96))
                        face_normalized = face_resized.astype('float32') / 255.0
                        face_input = np.expand_dims(face_normalized, axis=0)

                        # Predict emotions
                        preds = emotion_model.predict(face_input, verbose=0)[0]
                        emotion_idx = int(np.argmax(preds))
                        detected_emotion = EMOTIONS[emotion_idx]
                        max_confidence = preds[emotion_idx]

                        # Calculate stress
                        stress_level, stress_class, stress_pct = estimate_stress_from_emotion(detected_emotion, preds)

                        # Update session state
                        st.session_state.current_emotion = detected_emotion
                        st.session_state.current_stress = stress_level
                        st.session_state.current_confidence = int(max_confidence * 100)
                        st.session_state.latest_predictions = [float(p) for p in preds]

                        # Annotate frame (ASCII labels for OpenCV Hershey fonts)
                        frame = draw_emotion_overlay(
                            frame, x, y, w, h,
                            detected_emotion.capitalize(),
                            int(max_confidence * 100),
                            stress_level
                        )
                        break  # Analyze dominant face

                    # Render video frame
                    frame_placeholder.image(frame, channels="BGR", use_container_width=True)

                    if found_face:
                        icon = EMOTION_ICONS.get(st.session_state.current_emotion, "😐")
                        localized_em = get_emotion_label(st.session_state.current_emotion, curr_lang)
                        localized_st = get_stress_label(st.session_state.current_stress, curr_lang)

                        # Update emotion card
                        with emotion_placeholder.container():
                            st.markdown(f"""
                            <div class="result-card">
                                <h3>{get_text('detected_emotion', curr_lang)}</h3>
                                <div class="emotion-display">{icon}</div>
                                <div class="emotion-label">{localized_em}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        # Update stress card
                        with stress_placeholder.container():
                            st.markdown(f"""
                            <div class="result-card">
                                <h3>{get_text('stress_level', curr_lang)}</h3>
                                <div class="stress-indicator {stress_class}">
                                    {localized_st} ({stress_pct}%)
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        # Update confidence card
                        with confidence_placeholder.container():
                            st.markdown(f"""
                            <div class="result-card">
                                <h3>{get_text('confidence_level', curr_lang)}</h3>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {st.session_state.current_confidence}%;"></div>
                                </div>
                                <p style="text-align: center; color: #2C3E50; font-weight: 600; margin: 0;">{st.session_state.current_confidence}%</p>
                            </div>
                            """, unsafe_allow_html=True)

                        # Update Plotly breakdown chart
                        with chart_placeholder.container():
                            fig = render_emotion_chart(EMOTIONS, st.session_state.latest_predictions, language=curr_lang)
                            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                except Exception as e:
                    # Continue frame loop on non-critical detection errors
                    pass

                time.sleep(0.03)

            cap.release()
            status_box.success(get_text("status_ended", curr_lang))

# =========================================================================
# TAB 2: MindCare AI Wellness Chatbot
# =========================================================================
with tab_chat:
    render_wellness_chat(gemini_assistant, language=curr_lang)
