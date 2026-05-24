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

from src.black_scholes import price_option_black_scholes
from src.strategies import option_payoff

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="B-S Strategies · Derivatives Platform",
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

section[data-testid="stSidebar"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #555570 !important;
}

.sidebar-section {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #60a5fa;
    padding: 20px 0 8px 0;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 16px;
}

/* Page header */
.page-header {
    padding: 40px 8px 24px 8px;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 28px;
}

.page-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    color: #60a5fa;
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

/* Leg card */
.leg-card {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 20px 24px 16px 24px;
    margin-bottom: 12px;
    position: relative;
}

.leg-card.call-long  { border-left: 3px solid #4ade80; }
.leg-card.call-short { border-left: 3px solid #86efac; }
.leg-card.put-long   { border-left: 3px solid #f87171; }
.leg-card.put-short  { border-left: 3px solid #fca5a5; }

.leg-number {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #333350;
    margin-bottom: 12px;
}

.premium-display {
    display: flex;
    align-items: baseline;
    gap: 4px;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #1a1a2a;
}

.premium-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #333350;
}

.premium-value {
    font-family: 'DM Mono', monospace;
    font-size: 20px;
    font-weight: 500;
    color: #60a5fa;
    margin-left: 8px;
}

/* Section header */
.section-header {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #555570;
    margin: 32px 0 16px 0;
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

/* Selectbox / number input styling */
div[data-baseweb="select"] > div {
    background-color: #0f0f1a !important;
    border-color: #1e1e2e !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}

/* Slider */
.stSlider > div > div > div {
    color: #60a5fa !important;
}

/* Summary bar */
.summary-bar {
    display: flex;
    gap: 24px;
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 8px;
    padding: 16px 24px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}

.summary-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.summary-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #333350;
}

.summary-value {
    font-family: 'DM Mono', monospace;
    font-size: 15px;
    color: #c0c0d8;
}

.summary-value.positive { color: #4ade80; }
.summary-value.negative { color: #f87171; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown('<div class="sidebar-section">// Market Parameters</div>', unsafe_allow_html=True)

spot = st.sidebar.number_input("Spot Price (S0)", value=100.0)
risk_free_rate = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)
volatility = st.sidebar.number_input("Volatility (σ)", value=0.20)
maturity = st.sidebar.number_input("Time to Maturity (T)", value=1.0)

# ---------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------

st.markdown("""
<div class="page-header">
    <div class="page-eyebrow">// Black-Scholes Model</div>
    <div class="page-title">Strategy Builder</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# STRATEGY LEGS
# ---------------------------------------------------

st.markdown('<div class="section-header">Positions</div>', unsafe_allow_html=True)

num_legs = st.slider("Number of Positions", min_value=1, max_value=4, value=2, label_visibility="collapsed")

positions = []

# Color mapping for leg cards
def leg_class(side, opt_type):
    key = f"{opt_type.lower()}-{side.lower()}"
    return key  # call-long | call-short | put-long | put-short

for i in range(num_legs):

    col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.4, 1.0])

    with col1:
        position_side = st.selectbox(
            f"Side",
            ["Long", "Short"],
            key=f"side_{i}"
        )
    with col2:
        option_kind = st.selectbox(
            f"Type",
            ["Call", "Put"],
            key=f"type_{i}"
        )
    with col3:
        strike_input = st.number_input(
            f"Strike",
            value=100.0,
            key=f"strike_{i}"
        )
    with col4:
        quantity_input = st.number_input(
            f"Qty",
            min_value=1,
            value=1,
            key=f"qty_{i}"
        )

    result = price_option_black_scholes(
        S0=spot,
        K=strike_input,
        r=risk_free_rate,
        sigma=volatility,
        T=maturity,
        option_type=option_kind.lower(),
        q=0.0
    )
    premium = result["price"]
    d1 = result["d1"]
    d2 = result["d2"]

    card_class = leg_class(position_side, option_kind)
    sign = "+" if position_side == "Long" else "−"
    premium_color = "#4ade80" if option_kind == "Call" else "#f87171"

    st.markdown(f"""
    <div class="leg-card {card_class}">
        <div class="leg-number">Position {i+1} · {position_side} {option_kind} · K={strike_input:.0f} · x{quantity_input}</div>
        <div class="premium-display">
            <span class="premium-label">B-S Premium</span>
            <span class="premium-value" style="color:{premium_color};">{sign} {premium:.4f}</span>
            <span style="font-family:'DM Mono',monospace;font-size:10px;color:#333350;margin-left:16px;">
                d₁ = {d1:.4f} &nbsp;&nbsp; d₂ = {d2:.4f}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    positions.append({
        "side": position_side,
        "type": option_kind,
        "strike": strike_input,
        "premium": premium,
        "quantity": quantity_input
    })

# ---------------------------------------------------
# STRATEGY SUMMARY
# ---------------------------------------------------

total_cost = sum(
    p["premium"] * p["quantity"] * (1 if p["side"] == "Long" else -1)
    for p in positions
)
cost_class = "positive" if total_cost < 0 else "negative"
cost_label = "Net Credit" if total_cost < 0 else "Net Debit"

st.markdown(f"""
<div class="summary-bar">
    <div class="summary-item">
        <div class="summary-label">{cost_label}</div>
        <div class="summary-value {cost_class}">{abs(total_cost):.4f}</div>
    </div>
    <div class="summary-item">
        <div class="summary-label">Legs</div>
        <div class="summary-value">{num_legs}</div>
    </div>
    <div class="summary-item">
        <div class="summary-label">Spot S₀</div>
        <div class="summary-value">{spot:.2f}</div>
    </div>
    <div class="summary-item">
        <div class="summary-label">Volatility σ</div>
        <div class="summary-value">{volatility:.1%}</div>
    </div>
    <div class="summary-item">
        <div class="summary-label">Rate r</div>
        <div class="summary-value">{risk_free_rate:.1%}</div>
    </div>
    <div class="summary-item">
        <div class="summary-label">Maturity T</div>
        <div class="summary-value">{maturity:.2f}y</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# PAYOFF CHART
# ---------------------------------------------------

st.markdown('<div class="section-header">Payoff at Expiration</div>', unsafe_allow_html=True)

stock_prices = np.linspace(spot * 0.5, spot * 1.5, 600)
total_payoff = np.zeros_like(stock_prices)

fig = go.Figure()

# Color palette for individual legs
leg_colors = ["#60a5fa", "#a78bfa", "#fb923c", "#e879f9"]

for idx, position in enumerate(positions):

    payoff = option_payoff(
        stock_prices=stock_prices,
        strike=position["strike"],
        premium=position["premium"],
        option_type=position["type"].lower(),
        position=position["side"].lower(),
        quantity=position["quantity"]
    )
    total_payoff += payoff

    fig.add_trace(go.Scatter(
        x=stock_prices,
        y=payoff,
        mode="lines",
        name=f"P{idx+1} · {position['side']} {position['type']} K={position['strike']:.0f}",
        line=dict(color=leg_colors[idx % len(leg_colors)], width=1.5, dash="dot"),
        opacity=0.6
    ))

# Positive / Negative fill for total
positive_mask = total_payoff >= 0
negative_mask = total_payoff < 0

# Total line — green above zero, red below
fig.add_trace(go.Scatter(
    x=stock_prices,
    y=np.where(total_payoff >= 0, total_payoff, 0),
    mode="lines",
    name="Profit Zone",
    line=dict(color="#4ade80", width=0),
    fill="tozeroy",
    fillcolor="rgba(74, 222, 128, 0.08)",
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=stock_prices,
    y=np.where(total_payoff < 0, total_payoff, 0),
    mode="lines",
    name="Loss Zone",
    line=dict(color="#f87171", width=0),
    fill="tozeroy",
    fillcolor="rgba(248, 113, 113, 0.08)",
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=stock_prices,
    y=total_payoff,
    mode="lines",
    name="Total P&L",
    line=dict(
        color="#f0f0fa",
        width=2.5
    )
))

# Strike lines
for position in positions:
    fig.add_vline(
        x=position["strike"],
        line_dash="dot",
        line_color="rgba(100, 100, 150, 0.4)",
        line_width=1
    )

# Spot line
fig.add_vline(
    x=spot,
    line_dash="dash",
    line_color="rgba(96, 165, 250, 0.5)",
    line_width=1.5,
    annotation_text="S₀",
    annotation_font=dict(family="DM Mono, monospace", size=10, color="#60a5fa"),
    annotation_position="top"
)

# Zero line
fig.add_hline(
    y=0,
    line_color="rgba(80, 80, 120, 0.5)",
    line_width=1
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0f0f1a",
    plot_bgcolor="#0f0f1a",
    font=dict(family="DM Mono, monospace", color="#555570", size=11),
    title=dict(
        text="Strategy Payoff",
        font=dict(family="Syne, sans-serif", size=18, color="#c0c0d8"),
        x=0.0, xanchor="left"
    ),
    xaxis=dict(
        title="Underlying Price at Expiration",
        gridcolor="#131320",
        linecolor="#1e1e2e",
        tickfont=dict(family="DM Mono, monospace", size=10, color="#444460"),
        zeroline=False
    ),
    yaxis=dict(
        title="Profit / Loss",
        gridcolor="#131320",
        linecolor="#1e1e2e",
        tickfont=dict(family="DM Mono, monospace", size=10, color="#444460"),
        zeroline=False
    ),
    legend=dict(
        bgcolor="rgba(15,15,26,0.9)",
        bordercolor="#1e1e2e",
        borderwidth=1,
        font=dict(family="DM Mono, monospace", size=10, color="#888899")
    ),
    height=520,
    margin=dict(l=0, r=0, t=48, b=0),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
