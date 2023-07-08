"""

"""

###########
# IMPORTS #
###########
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gmean

####################
# HELPER FUNCTIONS #
####################

def _plot_bet1_distribution(ax, bet1, title):
    """
    Plot the distribution of outcomes of a dice roll.

    Arguments:
    - dice_outcomes: Array of dice outcomes

    Returns:
    None
    """
    # Values to percent
    results_percent = [(value - 1)* 100 for value in bet1.results]
    results_percent_labels = [f'{value:.0f}%' for value in results_percent]

    # Bar Plot
    ax.bar(results_percent_labels, bet1.weights, tick_label=results_percent_labels)

    # Setting labels and title
    ax.set_title('Xs and Os Profile: ' + title)
    ax.set_xlabel('--------------------------------------------------------------------------------')
    ax.set_ylabel(bet1.name.title() +' Distribution')

    # Set integer ticks on y-axis
    ax.set_yticks(range(0, max(bet1.weights)+1))

def _plot_bet_outcomes(ax, bet, marker):
    """
    This function takes in an Axes object and an array of dice outcomes, and plots the winning probabilities
    based on the dice outcomes on the Axes.

    Arguments:
    - ax: An Axes object where the plot will be drawn
    - dice_outcomes: An array containing the outcomes of dice rolls

    Returns:
    None
    """
    # Calculate the winning probabilities based on the dice outcomes
    win_probabilities = [(result - 1) * 100 for result in bet.results]

    # Prepare the categories for the x-axis
    categories = [str(int((result - 1) * 100)) + "%" for i, result in enumerate(bet.results)]
  
    # Plot the winning probabilities
    ax.plot(range(len(bet.results)), win_probabilities, marker=marker)  

    # Set the limits for the y-axis
    ax.set_ylim([min(win_probabilities) - 50, max(win_probabilities) + 50]) # Setting ylim dynamic to show whole graph

    # Set the label for the y-axis
    ax.set_ylabel(bet.name.title())  # the y-axis is labeled as "[bet_name] Roll"

    # Enable the grid
    ax.grid(True)

    # Set the labels for the x-axis
    ax.set_xticks(range(len(bet.results)))
    ax.set_xticklabels(categories)

    # Add annotations for arithmetic and geometric mean
    ax.text(0.02, 0.98, f'ARITHM AVG: {bet.arith_mean:.2f}%', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.88, f'GEOM AVG: {bet.geom_mean:.2f}%', transform=ax.transAxes, verticalalignment='top')

def _plot_combined_outcome(ax, bet_comparison):
    """
    This function plots the weighted average outcomes based on the provided ratio.

    Arguments:
    - ax: The subplot axis to draw on
    - dice_outcomes: A numpy array with the dice outcomes
    - cash_outcomes: A numpy array with the cash outcomes
    - dice_to_cash_ratio: A numpy array with two elements representing the weights for dice and cash

    Returns:
    None
    """
    # Calculate the winning probabilities based on the dice outcomes
    win_probabilities = [(result - 1) * 100 for result in bet_comparison.outcomes]

    # Prepare the categories for the x-axis
    categories = [str(int((result - 1) * 100)) + "%" for i, result in enumerate(bet_comparison.outcomes)]

    # Plot the weighted average outcomes
    ax.plot(categories, win_probabilities, marker='^')

    # Set the y-axis limits
    ax.set_ylim([-50, 100])

    # Set the y-axis label
    ax.set_ylabel(f"{bet_comparison.ratio[0] * 100} % {bet_comparison.bet1_name.title()} &\n {bet_comparison.ratio[1] * 100} % {bet_comparison.bet2_name.title()}")

    # Enable the grid
    ax.grid(True)

    # Remove x-axis labels
    ax.set_xticks([])

    # Add annotations for arithmetic and geometric mean
    #ax.text(0.02, 0.98, f'ARITHM AVG: {arith_mean_combined:.2f}%' + f' (Cost: {cost:.2f}%)', transform=ax.transAxes, verticalalignment='top')
    # ax.text(0.02, 0.88, f'GEOM AVG: {geom_mean_combined:.2f}%' + f' (Net: +{net:.2f}%)', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.98, f'ARITHM AVG: {bet_comparison.arith_mean_combined:.2f}%' + f' (Cost: {bet_comparison.cost:.2f}%)', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.88, f'GEOM AVG: {bet_comparison.geom_mean_combined:.2f}%' + f' (Net: {bet_comparison.net:.2f}%)', transform=ax.transAxes, verticalalignment='top')

############# 
# FUNCTIONS #
#############

def combined_outcomes(dice_outcomes, cash_outcomes, dice_to_cash_ratio):
    """
    Calculate combined outcomes of a combined wager of dice and cash at a given ratio.

    Args:
    dice_outcomes (array-like): Dice outcomes
    cash_outcomes (array-like): Cash outcomes
    dice_to_cash_ratio (array-like): Ratio of dice to cash

    Returns:
    array-like: Array of combined outcomes
    """
    return dice_to_cash_ratio[0] * dice_outcomes + dice_to_cash_ratio[1] * cash_outcomes


######### 
# PLOTS #
#########

def plot_xo_profile(bet1, bet2, bet_comparison, title):
    """
    This function calculates the weighted average for each pair of values in the 
    first two arrays based on the ratio in the third array.

    Arguments:
    - dice_outcomes: A numpy array with the dice outcomes
    - cash_outcomes: A numpy array with the cash outcomes
    - dice_to_cash_ratio: A numpy array with two elements representing the weights for dice and cash

    Return:
    None
    """
    # Create a figure with 4 subplots
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(4, 8))

    # Subplot 1: Distribution of bet1 outcomes
    _plot_bet1_distribution(ax1, bet1, title)

    # Subplot 2: Height of bet2 outcome
    _plot_bet_outcomes(ax2, bet1, 'x')

    # Subplot 3: Height of bet2 outcome
    _plot_bet_outcomes(ax3, bet2, 'o')

    # Subplot 4: Height of combined outcome
    _plot_combined_outcome(ax4, bet_comparison)

    # Adjust spacing between subplots
    plt.tight_layout()

    # Saving plot
    plt.savefig('../plots/xo_profile.png', dpi=300)

def plot_kelly_optimal(dice_outcomes, cash_outcomes):
    """
    This function takes dice and cash outcomes and plots the geometric mean 
    as a function of the fraction of wealth wagered per roll, thus visualising 
    the optimal Kelly bet size.
    
    Args:
    dice_outcomes (numpy array): Array of dice outcomes.
    cash_outcomes (numpy array): Array of cash outcomes.
    """
    # Define ratios ranging from 0 to 1 in steps of 0.01
    ratios = np.arange(0, 1.01, 0.01)
    geom_means = []
    
    # Iterate through the ratios
    for ratio in ratios:
        # Create ratio array for dice and cash
        dice_to_cash_ratio = np.array([ratio, 1-ratio])
        # Calculate geometric means
        geom_mean = (gmean(combined_outcomes(dice_outcomes, cash_outcomes, dice_to_cash_ratio)) - 1) * 100
        # Append geometric mean of combined outcomes to the list
        geom_means.append(geom_mean)
    
    # Find the maximum mean and its corresponding ratio
    max_mean = max(geom_means)
    max_ratio = ratios[geom_means.index(max_mean)]
    
    # Plotting the means
    plt.figure(figsize=(7, 3))  # Create a new figure with specified size
    plt.plot(ratios * 100, geom_means, label='Median')  # Plot geometric means
    plt.scatter(max_ratio * 100, max_mean)  # Mark the maximum with a scatter plot
    plt.text(max_ratio * 100, max_mean, f'Maximum at {max_ratio * 100}%')  # Add text indicating maximum
    
    # Set plot labels and title
    plt.xlabel('Percentage Of Wealth Wagered Per Roll')
    plt.ylabel('Geometric Average Return')
    plt.title('Finding The (Kelly) Optimal Bet Size')
    
    plt.legend()  # Show plot legend
    plt.grid(True)  # Show grid
    
    # Saving plot
    plt.savefig('../plots/kelly_optimal.png', dpi=300)
