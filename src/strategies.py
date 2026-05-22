import numpy as np


# ---------------------------------------------------
# GENERIC OPTION PAYOFF
# ---------------------------------------------------

def option_payoff(
    stock_prices,
    strike,
    premium,
    option_type="call",
    position="long",
    quantity=1
):

    # CALL
    if option_type.lower() == "call":

        payoff = np.maximum(
            stock_prices - strike,
            0
        ) - premium

    # PUT
    elif option_type.lower() == "put":

        payoff = np.maximum(
            strike - stock_prices,
            0
        ) - premium

    # SHORT POSITION
    if position.lower() == "short":

        payoff = -payoff

    return payoff * quantity