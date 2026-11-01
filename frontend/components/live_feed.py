"""
frontend/components/live_feed.py
Helper functions for webcam frame processing and visual annotations.
"""

import cv2

def draw_emotion_overlay(frame, x, y, w, h, emotion_text, confidence_pct, stress_text):
    """
    Draws a modern bounding box and status tag over a detected face in a video frame.
    """
    # Main bounding box
    cv2.rectangle(frame, (x, y), (x + w, y + h), (123, 222, 111), 2)

    # Top header badge: Emotion & Confidence
    label = f"{emotion_text} ({confidence_pct}%)"
    (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(frame, (x, max(0, y - text_h - 12)), (x + text_w + 10, y), (123, 222, 111), cv2.FILLED)
    cv2.putText(frame, label, (x + 5, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2)

    # Bottom badge: Stress Level
    stress_label = f"Stress: {stress_text}"
    (s_w, s_h), _ = cv2.getTextSize(stress_label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
    cv2.rectangle(frame, (x, y + h), (x + s_w + 10, y + h + s_h + 10), (74, 144, 226), cv2.FILLED)
    cv2.putText(frame, stress_label, (x + 5, y + h + s_h + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

    return frame

