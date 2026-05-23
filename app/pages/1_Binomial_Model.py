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
    page_title="Binomial Model",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.markdown("""
# 🌳 Binomial Tree Option Pricing
""")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown("## ⚙️ Option Configuration")

asset_type = st.sidebar.selectbox(
    "Underlying Asset",
    [
        "Stock",
        "Currency",
        "Dividend Paying Stock"
    ]
)

option_type = st.sidebar.selectbox(
    "Option Type",
    [
        "Call",
        "Put"
    ]
)

exercise_type = st.sidebar.selectbox(
    "Exercise Style",
    [
        "European",
        "American"
    ]
)

# ---------------------------------------------------
# MARKET PARAMETERS
# ---------------------------------------------------

st.sidebar.markdown("## 📊 Market Parameters")

spot = st.sidebar.number_input(
    "Spot Price (S0)",
    value=100.0
)

strike = st.sidebar.number_input(
    "Strike Price (K)",
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

steps = st.sidebar.number_input(
    "Number of Steps",
    min_value=1,
    value=1000
)

# ---------------------------------------------------
# DYNAMIC INPUTS
# ---------------------------------------------------

q = 0.0

if asset_type == "Currency":

    q = st.sidebar.number_input(
        "Foreign Interest Rate",
        value=0.02
    )

elif asset_type == "Dividend Paying Stock":

    q = st.sidebar.number_input(
        "Dividend Yield",
        value=0.03
    )

# ---------------------------------------------------
# BUTTON
# ---------------------------------------------------

calculate = st.sidebar.button(
    "Calculate Option Price"
)

# ---------------------------------------------------
# CALCULATION
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

    st.markdown("## 💰 Option Premium")

    st.metric(
        "Calculated Price",
        f"{option_price:.4f}"
    )

    # ---------------------------------------------------
    # CONVERGENCE
    # ---------------------------------------------------

    step_values = [
        5,
        10,
        25,
        50,
        100,
        250,
        500,
        1000
    ]

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

    fig.add_trace(
        go.Scatter(
            x=step_values,
            y=convergence_prices,
            mode="lines+markers",
            name="Binomial Price"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title="Binomial Convergence",
        xaxis_title="Steps",
        yaxis_title="Option Price",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )