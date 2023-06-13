"""


"""

###########
# IMPORTS #
###########
import math
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

##############
# FUNCTIIONS #
##############
def bev(payoffs, wealth_amount, bet_size):
    """
    Calculate the Bernoulli's Expected Value (BEV) corresponding to the given parameters.
    The BEV describes the expected ending value of the bet you are making (if the value is lower than the wealth amount, don't make that bet).

    Arguments:
    - payoffs: Possible payoffs of the bet
    - wealth_amount: Your current wealth
    - bet_size: The size of the bet you are making

    Returns:
    - bev: The Bernoulli's Expected Value (BEV) in the currency of your choice
    """
    # Calculate the ending wealth for each value of the bet
    end_wealth = [payoff + (wealth_amount - bet_size) for payoff in payoffs]
    # Calculate the average of the logarithms of all potential total ending wealth outcomes
    em = sum(math.log(payoff) for payoff in end_wealth) / len(end_wealth)
    # Calculate the exponential function of EM to obtain the BEV
    bev = math.exp(em)
    return bev

def betting_plot(payoffs, wealth_amount, bet_size):
    """
    Generate a plot to visualize the relationship between the fraction of starting wealth wagered
    and the ending wealth in the context of a betting scenario.

    Arguments:
    - payoffs: List of payoffs for each possible outcome of the bet
    - wealth_amount: Total wealth amount
    - bet_size: Size of the bet

    Returns:
    None
    """
    bet_range = []
    wealth_range = []

    for i in range(wealth_amount + 1):
        # Calculation of BEV (Expected Value of the Bet) for the current bet
        wager = bev(payoffs, wealth_amount, i)

        bet_range.append(i / wealth_amount * 100)  # Adding the percentage of wealth amount
        wealth_range.append(wager)

    # Create plot
    plt.plot(bet_range, wealth_range)
    plt.scatter(bet_size / wealth_amount * 100, wealth_range[bet_size], color='red', label='Optimal Bet')
    plt.plot([bet_size / wealth_amount * 100, bet_size / wealth_amount * 100], [0, wealth_range[bet_size]], color='red', linestyle='--')
    plt.plot([0, bet_size / wealth_amount * 100], [wealth_range[bet_size], wealth_range[bet_size]], color='red', linestyle='--')
    plt.xlabel('Fraction of Starting Wealth Wagered')
    plt.ylabel('Ending Wealth')
    plt.title('The Search for the Fair Value of the Petersburg Wager\nStarting Total Wealth: $100,000')
    plt.legend()

    # Set font properties for the text
    prop = fm.FontProperties(weight='bold')

    # Add text labels
    plt.text(bet_size / wealth_amount * 100, -0.05 * wealth_range[bet_size], f'{bet_size / wealth_amount * 100:.2f}%', ha='right', va='bottom')
    plt.text(bet_size / wealth_amount * 100 - 20, wealth_range[bet_size] + 0.05 * wealth_range[bet_size], f'${int(wealth_range[bet_size]):,}', ha='center', va='bottom', fontproperties=prop)

    plt.show()

def investment_recovery_plot(loss_value):
    """
    Plot the recovery percentage needed to get back to even after a loss assuming geometric growth

    Arguments:
    - loss_value: The loss percentage loss_value to plot

    Returns:
    None
    """
    # Loss percentage
    loss_range = range(-100, 0)

    # Percentage increase needed to recover the investment
    recovery_percent = [(1 / (1 + loss / 100) - 1) * 100 if loss != -100 else float('inf') for loss in loss_range]

    # Create the plot
    plt.plot(loss_range, recovery_percent)

    # Set axis labels and plot title
    plt.xlabel('Loss (%)')
    plt.ylabel('Profit to Get Back to Even (%)')
    plt.title('An Insidious Wealth Tax: The Greater the Loss, the Greater the Profit Needed to Get Back to Even')

    # Set the y-axis limit
    plt.ylim(top=2000, bottom=-100)

    # Plot the loss_value
    plt.plot(loss_value, recovery_percent[1 - abs(loss_value)], 'ro')
    plt.plot([loss_value, loss_value], [0, recovery_percent[1 - abs(loss_value)]], 'r--')
    plt.plot([loss_value, -100], [recovery_percent[1 - abs(loss_value)], recovery_percent[1 - abs(loss_value)]], 'r--')

    # Add text labels to the axes
    plt.text(loss_value + 5, -200, f'{loss_value}%', ha='right', va='bottom', color='black', fontsize=8)
    plt.text(-105, recovery_percent[1 - abs(loss_value)] - 40, f'{recovery_percent[1 - abs(loss_value)]:.2f}%', ha='right', va='bottom', color='black', fontsize=8)

    # Display the plot
    plt.show()
