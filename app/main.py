import streamlit as st
import sys
import os
import plotly.graph_objects as go

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from src.binomial_model import price_option_binomial

# ---------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------

st.set_page_config(
    page_title="Derivatives Pricing Platform",
    layout="wide"
)

# ---------------------------------------------------
# TÍTULO PRINCIPAL
# ---------------------------------------------------

st.markdown("""
# 📈 Derivatives Pricing Platform
### Binomial Tree Option Pricing Engine
""")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown("## ⚙️ Option Configuration")

# Tipo de activo
asset_type = st.sidebar.selectbox(
    "Underlying Asset",
    [
        "Stock",
        "Currency",
        "Dividend Paying Stock"
    ]
)

# Tipo de opción
option_type = st.sidebar.selectbox(
    "Option Type",
    [
        "Call",
        "Put"
    ]
)

# Tipo de ejercicio
exercise_type = st.sidebar.selectbox(
    "Exercise Style",
    [
        "European",
        "American"
    ]
)

# ---------------------------------------------------
# PARÁMETROS PRINCIPALES
# ---------------------------------------------------

st.sidebar.markdown("## 📊 Market Parameters")

spot = st.sidebar.number_input(
    "Spot Price (S0)",
    min_value=0.0,
    value=100.0
)

strike = st.sidebar.number_input(
    "Strike Price (K)",
    min_value=0.0,
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
# INPUTS DINÁMICOS
# ---------------------------------------------------

if asset_type == "Currency":

    foreign_rate = st.sidebar.number_input(
        "Foreign Interest Rate",
        value=0.02
    )

elif asset_type == "Dividend Paying Stock":

    dividend_yield = st.sidebar.number_input(
        "Dividend Yield",
        value=0.03
    )

# ---------------------------------------------------
# BOTÓN
# ---------------------------------------------------

calculate = st.sidebar.button("Calculate Option Price")

# ---------------------------------------------------
# PANEL PRINCIPAL
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Underlying",
        asset_type
    )

with col2:
    st.metric(
        "Option Type",
        option_type
    )

with col3:
    st.metric(
        "Exercise Style",
        exercise_type
    )

st.divider()

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Spot Price",
        f"{spot:.2f}"
    )

with col5:
    st.metric(
        "Strike Price",
        f"{strike:.2f}"
    )

with col6:
    st.metric(
        "Volatility",
        f"{volatility:.2%}"
    )

col7, col8, col9 = st.columns(3)

with col7:
    st.metric(
        "Risk-Free Rate",
        f"{risk_free_rate:.2%}"
    )

with col8:
    st.metric(
        "Maturity",
        f"{maturity:.2f} Years"
    )

with col9:
    st.metric(
        "Steps",
        f"{steps}"
    )

# ---------------------------------------------------
# PLACEHOLDER RESULTADO
# ---------------------------------------------------

if calculate:

    # Dividend Yield / Foreign Rate

    q = 0.0

    if asset_type == "Currency":

        q = foreign_rate

    elif asset_type == "Dividend Paying Stock":

        q = dividend_yield

    # Option Pricing

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
        # --------------------------------------------
    # CONVERGENCE ANALYSIS
    # --------------------------------------------

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

    # --------------------------------------------
    # OPTION PREMIUM
    # --------------------------------------------

    st.divider()

    st.markdown("## 💰 Option Premium")

    st.metric(
        label="Calculated Option Price",
        value=f"{option_price:.4f}"
    )

    # --------------------------------------------
    # PLOTLY CONVERGENCE CHART
    # --------------------------------------------

    st.divider()

    st.markdown("## 📈 Binomial Convergence Analysis")

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
        title="Binomial Model Convergence",
        xaxis_title="Number of Steps",
        yaxis_title="Option Price",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # Display Result

    if calculate:

        st.divider()

        st.markdown("## 💰 Option Premium")

        st.metric(
            label="Calculated Option Price",
            value=f"{option_price:.4f}"
        )
    