"""
frontend/components/stress_meter.py
Visual stress meter gauge component using Plotly.
"""

import plotly.graph_objects as go

def render_stress_gauge(stress_score, stress_level="Low"):
    """
    Renders an attractive circular gauge for stress score (0 to 100).
    """
    # Color mapping
    if stress_score < 30:
        bar_color = "#7BC96F"
    elif stress_score < 60:
        bar_color = "#F39C12"
    else:
        bar_color = "#E74C3C"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stress_score,
        title={'text': f"Stress Index: {stress_level}", 'font': {'size': 16, 'color': '#2C3E50'}},
        number={'suffix': "%", 'font': {'size': 24, 'color': bar_color}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#BDC3C7"},
            'bar': {'color': bar_color, 'thickness': 0.25},
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#ECF0F1",
            'steps': [
                {'range': [0, 30], 'color': '#E8F5E9'},
                {'range': [30, 60], 'color': '#FFF3E0'},
                {'range': [60, 100], 'color': '#FFEBEE'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 3},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))

    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif")
    )

    return fig

