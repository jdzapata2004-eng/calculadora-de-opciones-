import numpy as np

from scipy.stats import norm


# ---------------------------------------------------
# D1 AND D2
# ---------------------------------------------------

def calculate_d1_d2(
    S0,
    K,
    r,
    sigma,
    T,
    q=0.0
):

    d1 = (
        np.log(S0 / K)
        + (r - q + 0.5 * sigma**2) * T
    ) / (
        sigma * np.sqrt(T)
    )

    d2 = d1 - sigma * np.sqrt(T)

    return d1, d2
# ---------------------------------------------------
# GREEKS
# ---------------------------------------------------

def calculate_greeks(
    S0,
    K,
    r,
    sigma,
    T,
    option_type="call",
    q=0.0
):

    d1, d2 = calculate_d1_d2(
        S0,
        K,
        r,
        sigma,
        T,
        q
    )

    pdf_d1 = norm.pdf(d1)

    # -------------------------
    # DELTA
    # -------------------------

    if option_type.lower() == "call":

        delta = np.exp(-q * T) * norm.cdf(d1)

    else:

        delta = np.exp(-q * T) * (
            norm.cdf(d1) - 1
        )

    # -------------------------
    # GAMMA
    # -------------------------

    gamma = (
        np.exp(-q * T)
        * pdf_d1
        / (
            S0
            * sigma
            * np.sqrt(T)
        )
    )

    # -------------------------
    # VEGA
    # -------------------------

    vega = (
        S0
        * np.exp(-q * T)
        * pdf_d1
        * np.sqrt(T)
    )

    # -------------------------
    # THETA
    # -------------------------

    if option_type.lower() == "call":

        theta = (
            -(
                S0
                * np.exp(-q * T)
                * pdf_d1
                * sigma
            ) / (2 * np.sqrt(T))
            - r
            * K
            * np.exp(-r * T)
            * norm.cdf(d2)
            + q
            * S0
            * np.exp(-q * T)
            * norm.cdf(d1)
        )

    else:

        theta = (
            -(
                S0
                * np.exp(-q * T)
                * pdf_d1
                * sigma
            ) / (2 * np.sqrt(T))
            + r
            * K
            * np.exp(-r * T)
            * norm.cdf(-d2)
            - q
            * S0
            * np.exp(-q * T)
            * norm.cdf(-d1)
        )

    # -------------------------
    # RHO
    # -------------------------

    if option_type.lower() == "call":

        rho = (
            K
            * T
            * np.exp(-r * T)
            * norm.cdf(d2)
        )

    else:

        rho = (
            -K
            * T
            * np.exp(-r * T)
            * norm.cdf(-d2)
        )

    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho
    }

# ---------------------------------------------------
# BLACK-SCHOLES PRICING
# ---------------------------------------------------

def price_option_black_scholes(
    S0,
    K,
    r,
    sigma,
    T,
    option_type="call",
    q=0.0
):

    d1, d2 = calculate_d1_d2(
        S0,
        K,
        r,
        sigma,
        T,
        q
    )

    # --------------------------------------------
    # CALL OPTION
    # --------------------------------------------

    if option_type.lower() == "call":

        price = (
            S0 * np.exp(-q * T) * norm.cdf(d1)
            - K * np.exp(-r * T) * norm.cdf(d2)
        )

    # --------------------------------------------
    # PUT OPTION
    # --------------------------------------------

    elif option_type.lower() == "put":

        price = (
            K * np.exp(-r * T) * norm.cdf(-d2)
            - S0 * np.exp(-q * T) * norm.cdf(-d1)
        )

    greeks = calculate_greeks(
    S0,
    K,
    r,
    sigma,
    T,
    option_type,
    q
)

    return {
    "price": price,
    "d1": d1,
    "d2": d2,
    "delta": greeks["delta"],
    "gamma": greeks["gamma"],
    "vega": greeks["vega"],
    "theta": greeks["theta"],
    "rho": greeks["rho"]
}