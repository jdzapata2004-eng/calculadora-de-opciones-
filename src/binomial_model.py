import numpy as np


def price_option_binomial(
    S0,
    K,
    r,
    sigma,
    T,
    N,
    option_type="call",
    exercise_type="european",
    q=0.0
):
    """
    Prices an option using the Binomial Tree Model.

    Parameters
    ----------
    S0 : float
        Spot price of the underlying asset.

    K : float
        Strike price.

    r : float
        Risk-free interest rate.

    sigma : float
        Volatility of the underlying asset.

    T : float
        Time to maturity (in years).

    N : int
        Number of binomial steps.

    option_type : str
        "call" or "put".

    exercise_type : str
        "european" or "american".

    q : float
        Dividend yield or foreign interest rate.

    Returns
    -------
    float
        Option premium.
    """

    # ------------------------------------------------
    # BINOMIAL MODEL PARAMETERS
    # ------------------------------------------------

    dt = T / N

    u = np.exp(sigma * np.sqrt(dt))

    d = 1 / u

    p = (
        np.exp((r - q) * dt) - d
    ) / (u - d)
        # ------------------------------------------------
    # STOCK PRICE TREE
    # ------------------------------------------------

    stock_tree = np.zeros((N + 1, N + 1))

    for i in range(N + 1):

        for j in range(i + 1):

            stock_tree[j, i] = (
                S0
                * (u ** (i - j))
                * (d ** j)
            )
                # ------------------------------------------------
    # OPTION VALUE TREE
    # ------------------------------------------------

    option_tree = np.zeros((N + 1, N + 1))

    # Terminal payoff

    if option_type.lower() == "call":

        for j in range(N + 1):

            option_tree[j, N] = max(
                stock_tree[j, N] - K,
                0
            )

    elif option_type.lower() == "put":

        for j in range(N + 1):

            option_tree[j, N] = max(
                K - stock_tree[j, N],
                0
            )
                # ------------------------------------------------
    # BACKWARD INDUCTION
    # ------------------------------------------------

    for i in range(N - 1, -1, -1):

        for j in range(i + 1):

            continuation_value = np.exp(-r * dt) * (
                p * option_tree[j, i + 1]
                + (1 - p) * option_tree[j + 1, i + 1]
            )

            # European Option

            if exercise_type.lower() == "european":

                option_tree[j, i] = continuation_value

            # American Option

            elif exercise_type.lower() == "american":

                if option_type.lower() == "call":

                    intrinsic_value = max(
                        stock_tree[j, i] - K,
                        0
                    )

                elif option_type.lower() == "put":

                    intrinsic_value = max(
                        K - stock_tree[j, i],
                        0
                    )

                option_tree[j, i] = max(
                    continuation_value,
                    intrinsic_value
                )
    return option_tree[0, 0]
