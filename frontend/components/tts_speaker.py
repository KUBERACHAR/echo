"""
frontend/components/tts_speaker.py
Text-to-Speech (TTS) speaker component for chatbot responses.
Allows users to listen to MindCare assistant responses in English, Kannada, Hindi, and Telugu.
"""

import re
import json
import streamlit as st
import streamlit.components.v1 as components
from frontend.translations import get_text

LANG_CODE_MAP = {
    "English": "en-US",
    "Kannada": "kn-IN",
    "Hindi": "hi-IN",
    "Telugu": "te-IN"
}

def clean_text_for_speech(text: str) -> str:
    """
    Strips markdown formatting, URLs, code blocks, and list syntax
    to produce clean, natural spoken speech for TTS engines.
    """
    if not text:
        return ""
    # Remove code blocks
    cleaned = re.sub(r"```[\s\S]*?```", "", text)
    cleaned = re.sub(r"`[^`]*`", "", cleaned)
    # Remove markdown headers
    cleaned = re.sub(r"#{1,6}\s+", "", cleaned)
    # Remove markdown bold/italics
    cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"\*([^*]+)\*", r"\1", cleaned)
    # Remove markdown links, keeping label
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    # Remove list bullets and dashes
    cleaned = re.sub(r"(?m)^[\s*•\-–]+\s*", "", cleaned)
    # Remove horizontal rules
    cleaned = re.sub(r"[-=_]{3,}", "", cleaned)
    # Remove HTML tags if present
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    # Collapse multiple whitespaces/newlines into single spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def render_tts_button(text: str, language: str = "English", key: str = "tts"):
    """
    Renders a small, interactive speaker symbol button below an assistant response.
    Clicking the button plays audio speech using the browser's Web Speech API
    in the matching selected language (en-US, kn-IN, hi-IN, te-IN).
    """
    clean_text = clean_text_for_speech(text)
    if not clean_text:
        return

    lang_code = LANG_CODE_MAP.get(language, "en-US")
    listen_label = get_text("tts_listen", language, default="Listen")
    stop_label = get_text("tts_stop", language, default="Stop")
    tooltip = get_text("tts_tooltip", language, default="Listen to response")

    text_json = json.dumps(clean_text)
    listen_json = json.dumps(listen_label)
    stop_json = json.dumps(stop_label)
    lang_json = json.dumps(lang_code)

    html_code = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 2px 0;
    background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    display: flex;
    align-items: center;
    overflow: hidden;
  }}
  .speaker-btn {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #F8FAFC;
    color: #475569;
    border: 1px solid #CBD5E1;
    border-radius: 16px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    outline: none;
    transition: all 0.18s ease-in-out;
    user-select: none;
  }}
  .speaker-btn:hover {{
    background: #F1F5F9;
    color: #1E293B;
    border-color: #94A3B8;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
  }}
  .speaker-btn:active {{
    transform: translateY(0);
  }}
  .speaker-btn.speaking {{
    background: #E0F2FE;
    color: #0369A1;
    border-color: #38BDF8;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
  }}
  .icon {{
    font-size: 13px;
    line-height: 1;
    display: inline-block;
  }}
  .speaker-btn.speaking .icon {{
    animation: speakerPulse 1s infinite alternate ease-in-out;
  }}
  @keyframes speakerPulse {{
    from {{ transform: scale(1); }}
    to {{ transform: scale(1.18); }}
  }}
  .label {{
    line-height: 1.2;
    white-space: nowrap;
  }}
</style>
</head>
<body>
  <button id="speakerBtn" class="speaker-btn" title="{tooltip}" onclick="toggleSpeech()">
    <span id="speakerIcon" class="icon">🔊</span>
    <span id="speakerLabel" class="label">{listen_label}</span>
  </button>

  <script>
  (function() {{
    const textToSpeak = {text_json};
    const targetLang = {lang_json};
    const listenLabel = {listen_json};
    const stopLabel = {stop_json};

    const btn = document.getElementById("speakerBtn");
    const icon = document.getElementById("speakerIcon");
    const label = document.getElementById("speakerLabel");

    let isPlaying = false;
    let keepAliveTimer = null;

    function getSpeechSynth() {{
      try {{
        if (window.speechSynthesis) return window.speechSynthesis;
      }} catch(e) {{}}
      try {{
        if (window.parent && window.parent.speechSynthesis) return window.parent.speechSynthesis;
      }} catch(e) {{}}
      try {{
        if (window.top && window.top.speechSynthesis) return window.top.speechSynthesis;
      }} catch(e) {{}}
      return null;
    }}

    function resetUI() {{
      if (keepAliveTimer) {{
        clearInterval(keepAliveTimer);
        keepAliveTimer = null;
      }}
      isPlaying = false;
      btn.classList.remove("speaking");
      icon.textContent = "🔊";
      label.textContent = listenLabel;
    }}

    window.toggleSpeech = function() {{
      const synth = getSpeechSynth();
      if (!synth) {{
        alert("Text-to-speech is not supported in this browser.");
        return;
      }}

      // If already speaking this message, toggle stop
      if (isPlaying) {{
        synth.cancel();
        resetUI();
        return;
      }}

      // Stop any other active speech
      synth.cancel();
      resetUI();

      if (!textToSpeak || !textToSpeak.trim()) return;

      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      utterance.lang = targetLang;
      utterance.rate = 0.95;
      utterance.pitch = 1.0;

      // Select matching regional/language voice if available
      try {{
        const voices = synth.getVoices ? synth.getVoices() : [];
        if (voices && voices.length > 0) {{
          const langPrefix = targetLang.split("-")[0];
          const matchedVoice = voices.find(v => v.lang === targetLang) ||
                               voices.find(v => v.lang && v.lang.startsWith(langPrefix));
          if (matchedVoice) {{
            utterance.voice = matchedVoice;
          }}
        }}
      }} catch(e) {{}}

      utterance.onstart = function() {{
        isPlaying = true;
        btn.classList.add("speaking");
        icon.textContent = "⏹️";
        label.textContent = stopLabel;

        // Keepalive interval for long utterances in Chromium browsers
        keepAliveTimer = setInterval(function() {{
          if (!synth.speaking) {{
            clearInterval(keepAliveTimer);
            keepAliveTimer = null;
          }} else {{
            synth.pause();
            synth.resume();
          }}
        }}, 9000);
      }};

      utterance.onend = function() {{
        resetUI();
      }};

      utterance.onerror = function(event) {{
        // Canceled or interrupted is normal when stopping
        if (event && (event.error === "canceled" || event.error === "interrupted")) {{
          resetUI();
          return;
        }}
        console.warn("TTS notice:", event);
        resetUI();
      }};

      synth.speak(utterance);
    }};
  }})();
  </script>
</body>
</html>"""

    components.html(html_code, height=34, scrolling=False)

