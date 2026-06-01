# Derivatives Pricing & Risk Analytics Platform

> Interactive platform for option pricing, risk analysis, and strategy visualization built with Python and Streamlit.

---

## Overview

This project is a financial derivatives platform designed to price options, analyze risk exposures, and visualize multi-leg option strategies through an intuitive web interface.

The platform combines quantitative finance concepts with software engineering practices, providing an environment for exploring derivatives pricing models and portfolio risk metrics.

---

## Live Demo

🚀 Streamlit Application:

https://hxcvpjf23xtez4nvpo4fhq.streamlit.app

---

## Features

### Black-Scholes Pricing Engine

Price European options using the Black-Scholes model.

**Inputs**
- Spot Price (S₀)
- Strike Price (K)
- Risk-Free Rate (r)
- Volatility (σ)
- Time to Maturity (T)

**Outputs**
- Option Premium
- d₁
- d₂

---

### Greeks Analytics

Evaluate option sensitivity to market variables.

Implemented Greeks:

- Δ Delta
- Γ Gamma
- Vega
- Θ Theta
- Ρ Rho

Greeks are available:

- Per individual position
- Aggregated at portfolio/strategy level

---

### Multi-Leg Strategy Builder

Build and analyze custom option strategies.

Supported positions:

- Long Call
- Short Call
- Long Put
- Short Put

Features:

- Up to four simultaneous positions
- Dynamic payoff visualization
- Net Debit calculation
- Net Credit calculation
- Portfolio Greeks aggregation

Examples:

- Bull Call Spread
- Bear Put Spread
- Butterfly Spread
- Straddle
- Strangle
- Custom strategies

---

### Binomial Pricing Model

Alternative pricing framework using a recombining binomial tree.

Features:

- European Options
- American Options
- Adjustable number of steps
- Convergence Analysis
- Interactive Visualizations

---

## Risk Analytics

The platform allows users to evaluate strategy exposure through:

| Metric | Interpretation |
|----------|----------------|
| Delta | Sensitivity to underlying price changes |
| Gamma | Sensitivity of Delta |
| Vega | Sensitivity to volatility changes |
| Theta | Time decay |
| Rho | Sensitivity to interest rates |

---

## Technologies

### Programming

- Python

### Data & Quantitative Libraries

- NumPy
- SciPy

### Visualization

- Plotly

### Front-End

- Streamlit

### Version Control

- Git
- GitHub

---

## Project Structure

```text
derivatives-pricing-platform/
│
├── app/
│   ├── main.py                      # Home page
│   └── pages/
│       ├── 1_Binomial_Model.py      # Binomial Tree calculator
│       └── 2_Black_Scholes_Strategies.py  # B-S strategy builder
│
├── src/
│   ├── black_scholes.py             # B-S pricing + Greeks
│   ├── binomial_model.py            # Binomial Tree engine
│   └── strategies.py                # Multi-leg payoff logic
│
├── requirements.txt
└── README.md
│
└── pyproject.toml
```

---

## Mathematical Models

### Black-Scholes

The platform implements the classical Black-Scholes framework for European option valuation.

Key assumptions:

- Lognormal stock prices
- Constant volatility
- Constant risk-free rate
- No arbitrage opportunities
- Frictionless markets

---

### Binomial Tree Model

The binomial model approximates the evolution of the underlying asset through discrete time steps.

Advantages:

- Supports American options
- Flexible structure
- Educational visualization of pricing dynamics

---

## Motivation

This project was developed as part of my Financial Engineering training to strengthen practical skills in:

- Derivatives Pricing
- Quantitative Finance
- Risk Management
- Financial Modeling
- Python Development
- Financial Data Visualization

The objective is to bridge financial theory and software engineering through the construction of professional-grade analytical tools.

---

## Future Improvements

Planned features include:

- Break-even analysis
- Volatility scenario analysis
- Greeks heatmaps
- Implied volatility calculator
- Volatility smile visualization
- Monte Carlo pricing engine
- Historical volatility integration
- Portfolio risk dashboard

---

## Author

### Juan David Zapata Lopera

Financial Engineering Student  
Universidad de Medellín

Interested in:

- Quantitative Finance
- Financial Markets
- Derivatives
- Trading
- Risk Analytics
- Data Science

---

## License

This project is intended for educational and portfolio purposes.