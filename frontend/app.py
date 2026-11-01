# frontend/app.py
"""
MindCare - Real-Time Facial Emotion & Stress Detection with Mental Wellness Assistant.
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
        padding: 2.2rem 2rem 1.8rem 2rem;
        background: linear-gradient(135deg, #4A00E0 0%, #8E2DE2 50%, #5DADE2 100%);
        color: white;
        border-radius: 18px;
        margin-bottom: 1.5rem;
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
    
    .privacy-notice {
        background: linear-gradient(135deg, #E8F5E9 0%, #E3F2FD 100%);
        border-left: 5px solid #7BC96F;
        padding: 1rem 1.25rem;
        border-radius: 10px;
        margin: 0.5rem 0 1.5rem 0;
        border: 1px solid rgba(123, 201, 111, 0.25);
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
        font-size: 1.5rem;
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
    
    .telemetry-badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .badge-green { background: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }
    .badge-blue { background: #E3F2FD; color: #1565C0; border: 1px solid #90CAF9; }
    .badge-amber { background: #FFF8E1; color: #F57F17; border: 1px solid #FFE082; }
    .badge-red { background: #FFEBEE; color: #C62828; border: 1px solid #FFCDD2; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>ECHO</h1>
    <p>Real-Time Facial Mood & Stress Detection • Personalized Mental Wellness Chatbot</p>
</div>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
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

# --- Privacy Notice with Dismiss ---
# if st.session_state.show_privacy:
#     privacy_col1, privacy_col2 = st.columns([20, 1])
#     with privacy_col1:
#         st.markdown("""
#         <div class="privacy-notice">
#             <span style="font-size: 1.1rem;">🔒</span>
#             <strong>Your Privacy Matters:</strong> Video frames are analyzed locally in real-time. 
#             No video streams or images are saved to disk or transmitted over the internet.
#         </div>
#         """, unsafe_allow_html=True)
#     with privacy_col2:
#         if st.button("✕", key="dismiss_privacy", help="Dismiss notice"):
#             st.session_state.show_privacy = False
#             st.rerun()

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
    # Stress-associated emotions: angry (0), fear (2), sad (5)
    stress_emotions = [0, 2, 5]
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
    st.markdown("## MindCare AI Companion")
    
    # Assistant Status Badge
    if gemini_assistant.is_configured():
        st.markdown("""
        <div style="background: #E8F5E9; border-left: 4px solid #2E7D32; padding: 0.65rem 0.85rem; border-radius: 8px; margin-bottom: 0.8rem;">
            <strong style="color: #1B5E20; font-size: 0.95rem;">🟢 AI Assistant Active</strong><br>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #FFF8E1; border-left: 4px solid #F57F17; padding: 0.65rem 0.85rem; border-radius: 8px; margin-bottom: 0.8rem;">
            <strong style="color: #E65100; font-size: 0.95rem;">🟡 AI Assistant Ready</strong><br>
            <span style="font-size: 0.82rem; color: #5D4037;">Offline wellness mode active</span>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("⚙️ Assistant Settings"):
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
            "Creativity / Warmth",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.gemini_temp,
            step=0.05,
            help="Higher values make responses more conversational and warm."
        )
        if temp_val != st.session_state.gemini_temp:
            st.session_state.gemini_temp = temp_val
            gemini_assistant.set_temperature(temp_val)

        if st.button("🧪 Test AI Connection", use_container_width=True):
            with st.spinner("Pinging Gemini API..."):
                ok, msg = gemini_assistant.test_connection()
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    st.markdown("---")
    st.markdown("## 🎯 Stress Categories")
    st.markdown("""
    - 🟢 **Low:** Calm, balanced or joyful state
    - 🟡 **Medium:** Moderate strain or fatigue detected
    - 🔴 **High:** Heightened stress, tension, or distress
    """)

    st.markdown("---")
    st.markdown(f"**Model:** `{os.path.basename(MODEL_PATH)}`")
    st.caption("MindCare AI • Personalized Mental Wellness")

# --- Main Tabs ---
tab_monitor, tab_chat = st.tabs([
    "📹 Live Mood & Stress Tracker",
    "💬 MindCare AI Wellness Chatbot"
])

# =========================================================================
# TAB 1: Live Mood & Stress Tracker
# =========================================================================
with tab_monitor:
    col_video, col_metrics = st.columns([3, 2], gap="large")

    with col_video:
        st.markdown("### 📹 Live Webcam Feed")
        frame_placeholder = st.empty()

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            start_btn = st.button("▶ Start Detection", type="primary", use_container_width=True, key="start_det")
        with btn_col2:
            stop_btn = st.button("⏹ Stop Detection", use_container_width=True, key="stop_det")

        # Status badge below video
        status_box = st.empty()

    with col_metrics:
        st.markdown("### 📊 Real-Time Telemetry")
        emotion_placeholder = st.empty()
        stress_placeholder = st.empty()
        confidence_placeholder = st.empty()
        chart_placeholder = st.empty()
        recommendation_placeholder = st.empty()

        # Display initial / current metrics
        curr_icon = EMOTION_ICONS.get(st.session_state.current_emotion, "🤖")
        curr_em_label = st.session_state.current_emotion.capitalize() if st.session_state.current_emotion != "None" else "Waiting..."

        with emotion_placeholder.container():
            st.markdown(f"""
            <div class="result-card">
                <h3>Detected Emotion</h3>
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
                <h3>Stress Level</h3>
                <div class="stress-indicator {stress_style}">
                    {st.session_state.current_stress}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with confidence_placeholder.container():
            st.markdown(f"""
            <div class="result-card">
                <h3>Confidence Level</h3>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {st.session_state.current_confidence}%;"></div>
                </div>
                <p style="text-align: center; color: #2C3E50; font-weight: 600; margin: 0;">{st.session_state.current_confidence}%</p>
            </div>
            """, unsafe_allow_html=True)

        # Plotly Emotion Probability Chart
        with chart_placeholder.container():
            fig = render_emotion_chart(EMOTIONS, st.session_state.latest_predictions)
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
            st.error("❌ Could not access webcam. Please check your camera permissions and ensure no other application is using it.")
            st.session_state.detection_active = False
        else:
            status_box.info("🎥 Camera active. Real-time facial analysis in progress...")

            while st.session_state.detection_active:
                ret, frame = cap.read()
                if not ret:
                    st.warning("⚠️ Failed to capture video frame.")
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

                        # Annotate frame
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
                        # Update emotion card
                        with emotion_placeholder.container():
                            st.markdown(f"""
                            <div class="result-card">
                                <h3>Detected Emotion</h3>
                                <div class="emotion-display">{icon}</div>
                                <div class="emotion-label">{st.session_state.current_emotion.capitalize()}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        # Update stress card
                        with stress_placeholder.container():
                            st.markdown(f"""
                            <div class="result-card">
                                <h3>Stress Level</h3>
                                <div class="stress-indicator {stress_class}">
                                    {st.session_state.current_stress} ({stress_pct}%)
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        # Update confidence card
                        with confidence_placeholder.container():
                            st.markdown(f"""
                            <div class="result-card">
                                <h3>Confidence Level</h3>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {st.session_state.current_confidence}%;"></div>
                                </div>
                                <p style="text-align: center; color: #2C3E50; font-weight: 600; margin: 0;">{st.session_state.current_confidence}%</p>
                            </div>
                            """, unsafe_allow_html=True)

                        # Update Plotly breakdown chart
                        with chart_placeholder.container():
                            fig = render_emotion_chart(EMOTIONS, st.session_state.latest_predictions)
                            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                except Exception as e:
                    # Continue frame loop on non-critical detection errors
                    pass

                time.sleep(0.03)

            cap.release()
            status_box.success("✅ Detection session ended. State preserved.")

# =========================================================================
# TAB 2: MindCare AI Wellness Chatbot
# =========================================================================
with tab_chat:
    render_wellness_chat(gemini_assistant)


