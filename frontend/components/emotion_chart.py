"""
frontend/components/emotion_chart.py
Interactive emotion probability chart component using Plotly.
Supports localized labels based on selected language.
"""

import plotly.graph_objects as go
from frontend.translations import get_text, get_emotion_label

EMOTION_COLORS = {
    "angry": "#E74C3C",
    "disgust": "#8E44AD",
    "fear": "#E67E22",
    "happy": "#2ECC71",
    "neutral": "#95A5A6",
    "sad": "#3498DB",
    "surprise": "#F1C40F"
}

def render_emotion_chart(emotions, probabilities, language: str = "English"):
    """
    Renders an interactive horizontal bar chart of emotion probabilities.
    Labels dynamically reflect the selected language.
    """
    # Sort for best presentation
    pairs = sorted(zip(emotions, probabilities), key=lambda x: x[1])
    sorted_emotions = [get_emotion_label(p[0], lang=language) for p in pairs]
    sorted_probs = [round(p[1] * 100, 1) for p in pairs]
    colors = [EMOTION_COLORS.get(p[0].lower(), "#4A90E2") for p in pairs]

    fig = go.Figure(go.Bar(
        x=sorted_probs,
        y=sorted_emotions,
        orientation='h',
        marker=dict(color=colors, line=dict(width=1, color="rgba(0,0,0,0.1)")),
        text=[f"{val}%" for val in sorted_probs],
        textposition='outside',
        cliponaxis=False
    ))

    chart_title = get_text("chart_title", lang=language, default="Emotion Probability Breakdown")
    xaxis_title = get_text("chart_xaxis", lang=language, default="Probability (%)")

    fig.update_layout(
        title=chart_title,
        xaxis=dict(range=[0, 105], showgrid=True, gridcolor="rgba(0,0,0,0.05)", title=xaxis_title),
        yaxis=dict(showgrid=False),
        margin=dict(l=10, r=30, t=40, b=20),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif", size=12)
    )

    return fig
