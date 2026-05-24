import streamlit as st
import sys
import os
import plotly.graph_objects as go
import numpy as np

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

from src.binomial_model import price_option_binomial

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Binomial Tree · Derivatives Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}
.stApp { background: #0a0a0f; }

section[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e2e;
}

/* Sidebar labels */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stNumberInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #555570 !important;
}

/* Sidebar section headers */
.sidebar-section {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #4ade80;
    padding: 20px 0 8px 0;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 16px;
}

/* Main page header */
.page-header {
    padding: 40px 8px 24px 8px;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 32px;
}

.page-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    color: #4ade80;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 42px;
    font-weight: 800;
    color: #f0f0fa;
    letter-spacing: -1.5px;
    line-height: 1.1;
}

/* Result card */
.result-card {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 28px 32px;
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #4ade80, transparent);
}

.result-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #555570;
    margin-bottom: 8px;
}

.result-value {
    font-family: 'DM Mono', monospace;
    font-size: 48px;
    font-weight: 500;
    color: #4ade80;
    letter-spacing: -1px;
}

.result-unit {
    font-family: 'DM Mono', monospace;
    font-size: 14px;
    color: #333350;
    margin-left: 4px;
}

/* Parameter pills */
.param-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 32px;
}

.param-pill {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 8px;
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.param-pill-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #444460;
}

.param-pill-value {
    font-family: 'DM Mono', monospace;
    font-size: 18px;
    color: #c0c0d8;
    font-weight: 500;
}

/* Section header */
.section-header {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #555570;
    margin: 40px 0 20px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e1e2e;
}

/* Badge */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 4px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    gap: 5px;
}

.badge-call { background: #0d2b1a; color: #4ade80; border: 1px solid #1a4a2e; }
.badge-put  { background: #2b0d0d; color: #f87171; border: 1px solid #4a1a1a; }
.badge-euro { background: #0d1b2b; color: #60a5fa; border: 1px solid #1a2e4a; }
.badge-amer { background: #1e1a0d; color: #fbbf24; border: 1px solid #3a3010; }

.badges-row {
    display: flex;
    gap: 8px;
    margin-top: 12px;
}

/* Button override */
section[data-testid="stSidebar"] .stButton button {
    background: #4ade80 !important;
    color: #0a0a0f !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 12px 24px !important;
    width: 100% !important;
    margin-top: 8px !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    opacity: 0.85 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown('<div class="sidebar-section">// Option Config</div>', unsafe_allow_html=True)

asset_type = st.sidebar.selectbox(
    "Underlying Asset",
    ["Stock", "Currency", "Dividend Paying Stock"]
)

option_type = st.sidebar.selectbox(
    "Option Type",
    ["Call", "Put"]
)

exercise_type = st.sidebar.selectbox(
    "Exercise Style",
    ["European", "American"]
)

st.sidebar.markdown('<div class="sidebar-section">// Market Parameters</div>', unsafe_allow_html=True)

spot = st.sidebar.number_input("Spot Price (S0)", value=100.0)
strike = st.sidebar.number_input("Strike Price (K)", value=100.0)
risk_free_rate = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)
volatility = st.sidebar.number_input("Volatility (σ)", value=0.20)
maturity = st.sidebar.number_input("Time to Maturity (T)", value=1.0)
steps = st.sidebar.number_input("Number of Steps", min_value=1, value=1000)

q = 0.0
if asset_type == "Currency":
    q = st.sidebar.number_input("Foreign Interest Rate", value=0.02)
elif asset_type == "Dividend Paying Stock":
    q = st.sidebar.number_input("Dividend Yield", value=0.03)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
calculate = st.sidebar.button("▶  Calculate")

# ---------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------

option_color = "badge-call" if option_type == "Call" else "badge-put"
exercise_color = "badge-euro" if exercise_type == "European" else "badge-amer"

st.markdown(f"""
<div class="page-header">
    <div class="page-eyebrow">// Binomial Tree Model</div>
    <div class="page-title">Option Pricing</div>
    <div class="badges-row">
        <span class="badge {option_color}">{option_type}</span>
        <span class="badge {exercise_color}">{exercise_type}</span>
        <span class="badge" style="background:#1a1a2e;color:#8888aa;border:1px solid #2e2e4e;">{asset_type}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# PARAMETER SUMMARY
# ---------------------------------------------------

st.markdown(f"""
<div class="param-grid">
    <div class="param-pill">
        <div class="param-pill-label">Spot S₀</div>
        <div class="param-pill-value">{spot:.2f}</div>
    </div>
    <div class="param-pill">
        <div class="param-pill-label">Strike K</div>
        <div class="param-pill-value">{strike:.2f}</div>
    </div>
    <div class="param-pill">
        <div class="param-pill-label">Volatility σ</div>
        <div class="param-pill-value">{volatility:.1%}</div>
    </div>
    <div class="param-pill">
        <div class="param-pill-label">Rate r</div>
        <div class="param-pill-value">{risk_free_rate:.1%}</div>
    </div>
    <div class="param-pill">
        <div class="param-pill-label">Maturity T</div>
        <div class="param-pill-value">{maturity:.2f}y</div>
    </div>
    <div class="param-pill">
        <div class="param-pill-label">Steps N</div>
        <div class="param-pill-value">{int(steps)}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# RESULT
# ---------------------------------------------------

if calculate:

    option_price = price_option_binomial(
        S0=spot,
        K=strike,
        r=risk_free_rate,
        sigma=volatility,
        T=maturity,
        N=steps,
        option_type=option_type.lower(),
        exercise_type=exercise_type.lower(),
        q=q
    )

    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Calculated Option Premium</div>
        <div class="result-value">{option_price:.4f}<span class="result-unit">USD</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # CONVERGENCE
    # ---------------------------------------------------

    st.markdown('<div class="section-header">Convergence Analysis</div>', unsafe_allow_html=True)

    step_values = [5, 10, 25, 50, 100, 250, 500, 1000]
    convergence_prices = []

    for n_steps in step_values:
        price = price_option_binomial(
            S0=spot,
            K=strike,
            r=risk_free_rate,
            sigma=volatility,
            T=maturity,
            N=n_steps,
            option_type=option_type.lower(),
            exercise_type=exercise_type.lower(),
            q=q
        )
        convergence_prices.append(price)

    fig = go.Figure()

    # Shaded region around final value
    final = convergence_prices[-1]
    fig.add_hrect(
        y0=final * 0.995,
        y1=final * 1.005,
        fillcolor="rgba(74, 222, 128, 0.05)",
        line_width=0
    )

    fig.add_hline(
        y=final,
        line_dash="dot",
        line_color="rgba(74, 222, 128, 0.3)",
        line_width=1
    )

    fig.add_trace(go.Scatter(
        x=step_values,
        y=convergence_prices,
        mode="lines+markers",
        name="Binomial Price",
        line=dict(color="#4ade80", width=2),
        marker=dict(
            color="#0a0a0f",
            size=8,
            line=dict(color="#4ade80", width=2)
        ),
        fill="tozeroy",
        fillcolor="rgba(74, 222, 128, 0.04)"
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f0f1a",
        plot_bgcolor="#0f0f1a",
        font=dict(family="DM Mono, monospace", color="#555570", size=11),
        title=dict(
            text=f"Convergence to {final:.4f}",
            font=dict(family="Syne, sans-serif", size=16, color="#c0c0d8"),
            x=0.0, xanchor="left"
        ),
        xaxis=dict(
            title="Number of Steps",
            gridcolor="#1a1a2a",
            linecolor="#1e1e2e",
            tickfont=dict(family="DM Mono, monospace", size=10, color="#444460")
        ),
        yaxis=dict(
            title="Option Price",
            gridcolor="#1a1a2a",
            linecolor="#1e1e2e",
            tickfont=dict(family="DM Mono, monospace", size=10, color="#444460")
        ),
        height=420,
        margin=dict(l=0, r=0, t=48, b=0),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    # Empty state
    st.markdown("""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 320px;
        border: 1px dashed #1e1e2e;
        border-radius: 12px;
        gap: 12px;
    ">
        <div style="font-size: 32px;">🌳</div>
        <div style="font-family: 'DM Mono', monospace; font-size: 12px; color: #333350; letter-spacing: 0.15em; text-transform: uppercase;">
            Configure parameters and press Calculate
        </div>
    </div>
    """, unsafe_allow_html=True)
