"""
This module contains functions and helper functions for plotting data and necessary plots 
for understanding Safe Haven Investing.

Functions:
"""

# Import modules
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter
import seaborn as sns

# Defining functions
def investment_recovery(loss_value):
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



