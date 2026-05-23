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
    page_title="Black-Scholes Strategies",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.markdown("""
# 📊 Black-Scholes Strategies
""")

# ---------------------------------------------------
# MARKET PARAMETERS
# ---------------------------------------------------

st.sidebar.markdown("## 📈 Market Parameters")

spot = st.sidebar.number_input(
    "Spot Price (S0)",
    value=100.0
)

risk_free_rate = st.sidebar.number_input(
    "Risk-Free Rate (r)",
    value=0.05
)

volatility = st.sidebar.number_input(
    "Volatility (σ)",
    value=0.20
)

maturity = st.sidebar.number_input(
    "Time to Maturity (T)",
    value=1.0
)

# ---------------------------------------------------
# STRATEGY BUILDER
# ---------------------------------------------------

st.markdown("## ⚙️ Strategy Builder")

num_legs = st.slider(
    "Number of Positions",
    min_value=1,
    max_value=4,
    value=2
)

positions = []

for i in range(num_legs):

    st.markdown(f"### Position {i+1}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        position_side = st.selectbox(
            f"Side {i}",
            ["Long", "Short"]
        )

    with col2:

        option_kind = st.selectbox(
            f"Option Type {i}",
            ["Call", "Put"]
        )

    with col3:

        strike_input = st.number_input(
            f"Strike {i}",
            value=100.0
        )

    with col4:

        quantity_input = st.number_input(
            f"Quantity {i}",
            min_value=1,
            value=1
        )

    # --------------------------------------------
    # BLACK-SCHOLES PREMIUM
    # --------------------------------------------

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

    st.metric(
        f"Premium Position {i+1}",
        f"{premium:.4f}"
    )

    positions.append({
        "side": position_side,
        "type": option_kind,
        "strike": strike_input,
        "premium": premium,
        "quantity": quantity_input
    })

# ---------------------------------------------------
# PAYOFF DIAGRAM
# ---------------------------------------------------

st.divider()

st.markdown("## 📈 Strategy Payoff")

stock_prices = np.linspace(
    spot * 0.5,
    spot * 1.5,
    500
)

total_payoff = np.zeros_like(stock_prices)

fig = go.Figure()

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

    fig.add_trace(
        go.Scatter(
            x=stock_prices,
            y=payoff,
            mode="lines",
            name=f"Position {idx+1}"
        )
    )

# TOTAL STRATEGY

fig.add_trace(
    go.Scatter(
        x=stock_prices,
        y=total_payoff,
        mode="lines",
        name="Total Strategy",
        line=dict(width=5)
    )
)

fig.add_hline(
    y=0,
    line_dash="dash"
)

fig.update_layout(
    template="plotly_dark",
    title="Options Strategy Payoff",
    xaxis_title="Underlying Price at Expiration",
    yaxis_title="Profit / Loss",
    height=650
)

st.plotly_chart(
    fig,
    use_container_width=True
)