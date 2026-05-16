import streamlit as st
import sys
import os

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

st.title("📈 Derivatives Pricing Platform")
st.markdown("### Binomial Tree Option Pricing Model")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Option Configuration")

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

st.sidebar.header("Market Parameters")

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

st.subheader("Selected Configuration")

st.write(f"Underlying Asset: {asset_type}")
st.write(f"Option Type: {option_type}")
st.write(f"Exercise Style: {exercise_type}")

st.subheader("Current Parameters")

st.write(f"Spot Price: {spot}")
st.write(f"Strike Price: {strike}")
st.write(f"Risk-Free Rate: {risk_free_rate}")
st.write(f"Volatility: {volatility}")
st.write(f"Time to Maturity: {maturity}")
st.write(f"Steps: {steps}")

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

    # Display Result

    st.subheader("Option Premium")

    st.success(f"Option Price: {option_price:.4f}")