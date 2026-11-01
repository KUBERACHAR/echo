"""
config.py
Developer Configuration File for MindCare AI.

Set your Google Gemini API Key here so end-users can directly access the LLM
without needing to configure or enter any API keys themselves.
"""

import os
from pathlib import Path

# Load .env file if present
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))
    except Exception:
        pass

# =============================================================================
# 🔑 DEVELOPER GEMINI API KEY
# =============================================================================
# Set your Gemini API key below, or set the environment variable GEMINI_API_KEY:
DEVELOPER_GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Final resolved API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", DEVELOPER_GEMINI_API_KEY).strip()

# Gemini model settings (use active Gemini 3.x models)
DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"
DEFAULT_TEMPERATURE = 0.7

