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

def _weighted_average(dice_outcomes, cash_outcomes, dice_to_cash_ratio):
    """
    This function calculates the weighted average for each pair of values in the 
    first two arrays based on the ratio in the third array.
    
    Arguments:
    - dice_outcomes: A numpy array with the dice outcomes
    - cash_outcomes: A numpy array with the cash outcomes
    - dice_to_cash_ratio: A numpy array with two elements representing the weights for dice and cash
    
    Return:
    - A numpy array with the weighted averages
    """
    
     # Make sure all arrays have the same length
    assert len(dice_outcomes) == len(cash_outcomes), "The first two arrays must have the same length"
    assert len(dice_to_cash_ratio) == 2, "The ratio array must have exactly two elements"

    dice_weight, cash_weight = dice_to_cash_ratio
    weighted_averages = []

    for dice, cash in zip(dice_outcomes, cash_outcomes):
        weighted_average = dice * dice_weight + cash * cash_weight
        weighted_averages.append(weighted_average)

    return np.array(weighted_averages)


def _dice_distribution(ax, dice_outcomes):
    """
    Plot the distribution of outcomes of a dice roll.

    Arguments:
    - dice_outcomes: Array of dice outcomes

    Returns:
    None
    """
    # Calculate unique values and their counts
    unique_values, counts = np.unique(dice_outcomes, return_counts=True)

    # Convert unique values to percentage and add % sign
    unique_values = [(value - 1) * 100 for value in unique_values]
    unique_values = [f'{value:.0f}% ' for value in unique_values]

    # Plot the bar chart
    ax.bar(unique_values, counts)
    ax.set_xlabel('--------------------------------------------------------------------------------')
    ax.set_ylabel('Dice Roll Distribution')
    ax.set_title('Xs and Os Profile: The Kelly Criterion')
    ax.set_yticks(np.arange(min(counts), max(counts) + 1, 1))  # Set integer ticks on y-axis

def _dice_outcome(ax, dice_outcomes, arith_dict, geom_dict):
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
    win_probabilities_dice = [(outcome - 1.0) * 100 for outcome in dice_outcomes]

    # Prepare the categories for the x-axis
    categories_dice = [str((outcome - 1) * 100) + "%" for outcome in dice_outcomes]

    # Plot the winning probabilities
    ax.plot(categories_dice, win_probabilities_dice, marker='x')  # 'x' marker is used

    # Set the limits for the y-axis
    ax.set_ylim([-50, 100])  # the limits are set from -50 to 100

    # Set the label for the y-axis
    ax.set_ylabel("Dice Roll")  # the y-axis is labeled as "[dice_name] Roll"

    # Enable the grid
    ax.grid(True)

    # Remove x-axis labels
    ax.set_xticks([])
    
    # Get arithmetic and geometric mean of dice outcomes
    arith_mean_dice = arith_dict.get('arith_mean_dice')
    geom_mean_dice = geom_dict.get('geom_mean_dice')

    # Add annotations for arithmetic and geometric mean
    ax.text(0.02, 0.98, f'ARITHM AVG: {arith_mean_dice:.2f}%', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.88, f'GEOM AVG: {geom_mean_dice:.2f}%', transform=ax.transAxes, verticalalignment='top')

def _cash_outcome(ax, dice_outcomes, cash_outcomes, arith_dict, geom_dict):
    """
    This function creates a subplot of cash outcomes based on the provided dice and cash outcomes.

    Arguments:
    - ax: A matplotlib.axes.Axes object. The plot will be drawn on this Axes.
    - dice_outcomes: A numpy array with the dice outcomes
    - cash_outcomes: A numpy array with the cash outcomes

    Return:
    None
    """
    # Determine the number of unique categories based on dice outcomes
    n_categories = len(np.unique(dice_outcomes))

    # Reshape cash outcomes according to the number of categories
    cash_outcomes_reshaped = np.array_split(cash_outcomes, n_categories)

    # Calculate the winning probabilities for cash outcomes
    win_probabilities_cash = [(np.mean(outcome) - 1.0) * 100 for outcome in cash_outcomes_reshaped]

    # Create categories for cash outcomes
    categories_cash = [str(i+1) for i, _ in enumerate(cash_outcomes_reshaped)]

    # Create a plot with 'o' as a marker
    ax.plot(categories_cash, win_probabilities_cash, marker='o')

    # Set the limit for the y-axis
    ax.set_ylim([-50, 100])

    # Set the label for the y-axis
    ax.set_ylabel("Cash")

    # Set the x-axis label
    ax.set_xlabel('=====================================================================================')

    # Enable grid
    ax.grid(True)

    # Remove x-axis labels
    ax.set_xticks([])

    # Calculate the arithmetic and geometric mean of the dice outcomes
    arith_mean_cash = arith_dict.get('arith_mean_cash')
    geom_mean_cash = geom_dict.get('geom_mean_cash')

    # Add annotations for arithmetic and geometric mean
    ax.text(0.02, 0.98, f'ARITHM AVG: {arith_mean_cash:.2f}%', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.88, f'GEOM AVG: {geom_mean_cash:.2f}%', transform=ax.transAxes, verticalalignment='top')

def _combined_outcome(ax, dice_outcomes, cash_outcomes, dice_to_cash_ratio, arith_dict, geom_dict):
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
    # Calculate the weighted average of the outcomes
    weighted_avg_outcomes = _weighted_average(dice_outcomes, cash_outcomes, dice_to_cash_ratio)
    
    # Convert outcomes to percentage probabilities
    win_probabilities_weighted = [(outcome - 1.0) * 100 for outcome in weighted_avg_outcomes]

    # Convert outcomes to percentage categories for plotting
    categories_weighted = [str((outcome - 1) * 100) + "%" for outcome in weighted_avg_outcomes]

    # Plot the weighted average outcomes
    ax.plot(categories_weighted, win_probabilities_weighted, marker='^')

    # Set the y-axis limits
    ax.set_ylim([-50, 100])

    # Set the y-axis label
    ax.set_ylabel(f"{dice_to_cash_ratio[0] * 100} % Dice Roll and " + f"{dice_to_cash_ratio[1] * 100} % Cash")

    # Enable the grid
    ax.grid(True)

    # Remove x-axis labels
    ax.set_xticks([])

    # Calculate the arithmetic and geometric mean of the dice outcomes
    arith_mean_combined = arith_dict.get('arith_mean_combined')
    geom_mean_combined = geom_dict.get('geom_mean_combined')

    cost = arith_dict.get('cost')
    net = geom_dict.get('net')

    # Add annotations for arithmetic and geometric mean
    #ax.text(0.02, 0.98, f'ARITHM AVG: {arith_mean_combined:.2f}%' + f' (Cost: {cost:.2f}%)', transform=ax.transAxes, verticalalignment='top')
    # ax.text(0.02, 0.88, f'GEOM AVG: {geom_mean_combined:.2f}%' + f' (Net: +{net:.2f}%)', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.98, f'ARITHM AVG: {arith_mean_combined:.2f}%' + f' (Cost: {cost:.2f}%)', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.88, f'GEOM AVG: {geom_mean_combined:.2f}%' + f' (Net: {net:.2f}%)', transform=ax.transAxes, verticalalignment='top')

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

def weighted_arith_mean(dice_outcomes, cash_outcomes, dice_to_cash_ratio):
    """
    Calculate arithmetic mean of a combined wager of dice and cash.
    
    Args:
    dice_outcomes (array-like): Dice outcomes
    cash_outcomes (array-like): Cash outcomes
    dice_to_cash_ratio (array-like): Ratio of dice to cash
    
    Returns:
    dict: Dictionary containing the calculated arithmetic means
    """
    
    # Calculate the arithmetic mean for dice and cash outcomes separately
    arith_mean_dice = (np.mean(dice_outcomes) - 1) * 100
    arith_mean_cash = (np.mean(cash_outcomes) - 1) * 100
    
    # Combine the outcomes based on the given ratio and calculate the arithmetic mean
    combined_outcomes = dice_to_cash_ratio[0] * dice_outcomes + dice_to_cash_ratio[1] * cash_outcomes
    arith_mean_combined = (np.mean(combined_outcomes) - 1) * 100
    
    # Calculate the cost
    cost = arith_mean_combined - arith_mean_dice - arith_mean_cash
    
    # Return a dictionary containing the calculated means
    arith_dict = {
        'arith_mean_dice': arith_mean_dice,
        'arith_mean_cash': arith_mean_cash,
        'arith_mean_combined': arith_mean_combined,
        'cost': cost
    }
    return arith_dict

def weighted_geom_mean(dice_outcomes, cash_outcomes, dice_to_cash_ratio):
    """
    Calculate geometric mean of a combined wager of dice and cash.
    
    Args:
    dice_outcomes (array-like): Dice outcomes
    cash_outcomes (array-like): Cash outcomes
    dice_to_cash_ratio (array-like): Ratio of dice to cash
    
    Returns:
    dict: Dictionary containing the calculated geometric means
    """
    
    # Check if the input arrays are of the same length
    assert len(dice_outcomes) == len(cash_outcomes), 'Arrays must be of the same length.'
    
    # Check if the sum of the ratio is equal to 1
    assert np.isclose(np.sum(dice_to_cash_ratio), 1), 'Ratio must sum to 1.'
    
    # Calculate the geometric mean for dice and cash outcomes separately
    geom_mean_dice = (gmean(dice_outcomes) - 1) * 100
    geom_mean_cash = (gmean(cash_outcomes) - 1) * 100
    
    # Combine the outcomes based on the given ratio and calculate the geometric mean
    combined_outcomes = dice_to_cash_ratio[0] * dice_outcomes + dice_to_cash_ratio[1] * cash_outcomes
    geom_mean_combined = (gmean(combined_outcomes) - 1) * 100
    
    # Calculate the net
    net = geom_mean_combined - geom_mean_dice - geom_mean_cash
    
    # Return a dictionary containing the calculated means
    geom_dict = {
        'geom_mean_dice': geom_mean_dice,
        'geom_mean_cash': geom_mean_cash,
        'geom_mean_combined': geom_mean_combined,
        'net': net
    }
    return geom_dict


def plot_xo_profile(dice_outcomes, cash_outcomes, dice_to_cash_ratio, arith_dict, geom_dict):
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

    # Subplot 1: Distribution of dice outcomes
    _dice_distribution(ax1, dice_outcomes)

    # Subplot 2: Height of dice outcome
    _dice_outcome(ax2, dice_outcomes, arith_dict, geom_dict)

    # Subplot 3: Height of cash outcome
    _cash_outcome(ax3, dice_outcomes, cash_outcomes, arith_dict, geom_dict)

    # Subplot 4: Height of combined outcome
    _combined_outcome(ax4, dice_outcomes, cash_outcomes, dice_to_cash_ratio, arith_dict, geom_dict)

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
        geom_dict = weighted_geom_mean(dice_outcomes, cash_outcomes, dice_to_cash_ratio)
        # Append geometric mean of combined outcomes to the list
        geom_means.append(geom_dict['geom_mean_combined'])
    
    # Find the maximum mean and its corresponding ratio
    max_mean = max(geom_means)
    max_ratio = ratios[geom_means.index(max_mean)]
    
    # Plotting the means
    plt.figure(figsize=(10, 6))  # Create a new figure with specified size
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
