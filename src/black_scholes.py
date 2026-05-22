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

    return {
        "price": price,
        "d1": d1,
        "d2": d2
    }