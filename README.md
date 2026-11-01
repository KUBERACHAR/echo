# MindCare: Real-Time Mood & Stress Detection with Gemini Mental Wellness AI

A comprehensive real-time facial emotion recognition, stress estimation, and personalized mental wellness companion powered by Deep Learning and Google Gemini LLM.

The application captures webcam video to detect faces, recognizes 7 core emotions (angry, disgust, fear, happy, neutral, sad, surprise), estimates stress and confidence levels, and connects users to an empathetic **Personalized Mental Wellness Chatbot** powered by Gemini LLM.

---

## 🌟 Features

- **Real-Time Facial Emotion Detection:** Identifies emotions using MTCNN and a pre-trained Keras/TensorFlow deep neural network (`emotion_model.h5`).
- **Stress & Confidence Estimation:** Real-time stress scoring (Low, Medium, High) with visual gauge and confidence tracking.
- **Personalized Mental Wellness Chatbot (Gemini LLM):**
  - Empathetic AI wellness companion ("MindCare Companion") powered by Google Gemini (`gemini-3.5-flash-lite`, `gemini-3.8-flash`).
  - **Dynamic Emotional Context Sync:** Adapts responses based on real-time detected facial emotion, stress levels, and confidence telemetry.
  - Interactive quick-wellness prompts (e.g., Box Breathing, Stress Relief, Affirmations, Desk Stretches).
  - Conversation history clearing.
- **Multi-Language Support (Dynamic UI & Chatbot):**
  - Instant one-click language selection buttons for **English (default)**, **Kannada (ಕನ್ನಡ)**, **Hindi (हिन्दी)**, and **Telugu (తెలుగు)**.
  - Dynamically localizes all interface elements: headers, tabs, camera controls, live telemetry cards, charts, and quick wellness starters.
  - Generates culturally empathetic and linguistically accurate chatbot responses in the chosen language.
- **Interactive Streamlit Dashboard:** Modern, calming wellness UI with multi-tab layout and Plotly emotion probability distributions.

---

## 📁 Project Structure

```text
VIDEO-MOOD-STRESS/
├── backend/
│   ├── ml/
│   │   ├── emotion_model.py     # Model loading and compilation
│   │   ├── face_detector.py     # DeepFace/MTCNN face detection
│   │   ├── stress_score.py      # Stress heuristic calculations
│   │   └── __init__.py
│   ├── utils/
│   │   └── video_utils.py       # Video utility functions
│   ├── gemini_service.py        # Gemini LLM wellness service (REST & SDK)
│   └── main.py                  # CLI test runner for video/image
├── frontend/
│   ├── components/
│   │   ├── emotion_chart.py     # Plotly emotion probability bar chart
│   │   ├── live_feed.py         # Frame drawing and face overlay helpers
│   │   ├── stress_meter.py      # Circular stress gauge component
│   │   └── wellness_chat.py     # Interactive Gemini wellness chat UI
│   └── app.py                   # Main Streamlit web application
├── models/
│   └── emotion_model.h5         # Pre-trained emotion classification model
├── requirements.txt             # Python project dependencies
└── README.md                    # Project documentation
```

---

## ⚙️ Requirements & Prerequisites

- **Python:** 3.11 or 3.12 (Recommended: 3.12)
- **Webcam:** Any standard USB or built-in webcam
- **Google Gemini API Key:** Free key from [Google AI Studio](https://aistudio.google.com/)

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <REPO_URL>
   cd echo
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```powershell
     python -m venv myenv
     .\myenv\Scripts\Activate.ps1
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv myenv
     source myenv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Developer API Key (One-time Developer Setup):**
   - Open `config.py` in the project root and insert your Gemini API Key:
     ```python
     DEVELOPER_GEMINI_API_KEY = "your_actual_gemini_api_key_here"
     ```
   - Alternatively, rename `.env.example` to `.env` and set:
     ```env
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     ```
   - *End-users do not need to configure any keys—they can directly open the app and chat!*

---

## 🖥️ How to Run

1. **Launch the Streamlit Dashboard:**
   ```bash
   streamlit run frontend/app.py
   ```
2. The web browser will automatically open at `http://localhost:8501`.
3. **User Experience:**
   - **Zero Technical Configuration:** The user does not need to enter any API keys or credentials.
   - **Live Mood & Stress Tracker Tab:** Click **▶ Start Detection** to analyze facial expressions, stress levels, and confidence in real time.
   - **MindCare AI Wellness Chatbot Tab:** Directly chat with the Personalized Mental Wellness Assistant. The chatbot automatically utilizes real-time detected facial emotion and stress telemetry to provide empathetic, context-aware responses.
   - **Quick Starters:** Users can tap one-click prompt chips for immediate 2-minute box breathing, stress relief, affirmations, or workday resets.
   - Use one-click quick starters for guided breathing, grounding, or affirmations.

---

## 🔬 How It Works

1. **Face Detection:** MTCNN scans webcam frames for human faces and outputs bounding boxes.
2. **Emotion Recognition:** The detected face is normalized to $96 \times 96 \times 3$ and evaluated by `emotion_model.h5`, generating probabilities across 7 emotions.
3. **Stress Estimation:** Probabilities of stress-associated emotions (angry, fear, sad) are computed to categorize stress into Low, Medium, or High.
4. **Gemini LLM Personalization:** The detected state is seamlessly injected into the Gemini API conversational prompt, enabling compassionate, tailored mental wellness responses.

---

## 🛡️ Privacy & Safety Disclaimer

- **Local Processing:** All webcam video frames are processed locally on your machine and are never uploaded or stored.
- **Mental Wellness Scope:** MindCare is an educational and supportive wellness tool, not a medical or clinical diagnosis system. If in distress, please contact national emergency services or crisis lines (e.g., 988 in the US/Canada, 14416 Tele-MANAS in India, 111 in the UK).
