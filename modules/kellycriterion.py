"""

"""

# Import modules
import matplotlib.pyplot as plt
import numpy as np

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

def _dice_outcome(ax, dice_outcomes):
    """
    This function takes in an Axes object and an array of dice outcomes, and plots the winning probabilities
    based on the dice outcomes on the Axes.

    Arguments:
    - ax: An Axes object where the plot will be drawn
    - dice_outcomes: An array containing the outcomes of dice rolls

    Returns:
    None
    """
    
    # Extract the variable name of the dice outcomes for labeling purposes
    dice_name = extract_variable_name(dice_outcomes, globals())

    # Calculate the winning probabilities based on the dice outcomes
    win_probabilities_dice = [(outcome - 1.0) * 100 for outcome in dice_outcomes]

    # Prepare the categories for the x-axis
    categories_dice = [str((outcome - 1) * 100) + "%" for outcome in dice_outcomes]

    # Plot the winning probabilities
    ax.plot(categories_dice, win_probabilities_dice, marker='x')  # 'x' marker is used

    # Set the limits for the y-axis
    ax.set_ylim([-50, 100])  # the limits are set from -50 to 100

    # Set the label for the y-axis
    ax.set_ylabel(dice_name + " Roll")  # the y-axis is labeled as "[dice_name] Roll"

    # Enable the grid
    ax.grid(True)

    # Remove x-axis labels
    ax.set_xticks([])
    
    # Get arithmetic and geometric mean of dice outcomes
    arith_mean_dice = df_kelly.at['dice_roll', 'arith_avg']
    geom_mean_dice = df_kelly.at['dice_roll', 'geom_avg']

    # Add annotations for arithmetic and geometric mean
    ax.text(0.02, 0.98, f'ARITHM AVG: {arith_mean_dice:.2f}%', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.88, f'GEOM AVG: {geom_mean_dice:.2f}%', transform=ax.transAxes, verticalalignment='top')

def _cash_outcome(ax, dice_outcomes, cash_outcomes):
    """
    This function creates a subplot of cash outcomes based on the provided dice and cash outcomes.

    Arguments:
    - ax: A matplotlib.axes.Axes object. The plot will be drawn on this Axes.
    - dice_outcomes: A numpy array with the dice outcomes
    - cash_outcomes: A numpy array with the cash outcomes

    Return:
    None
    """

    # Extract the variable name of cash_outcomes
    cash_name = extract_variable_name(cash_outcomes, globals())

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
    ax.set_ylabel(cash_name)

    # Set the x-axis label
    ax.set_xlabel('=====================================================================================')

    # Enable grid
    ax.grid(True)

    # Remove x-axis labels
    ax.set_xticks([])

    # Calculate the arithmetic and geometric mean of the dice outcomes
    arith_mean_cash = df_kelly.at['cash', 'arith_avg']
    geom_mean_cash = df_kelly.at['cash', 'geom_avg']

    # Add annotations for arithmetic and geometric mean
    ax.text(0.02, 0.98, f'ARITHM AVG: {arith_mean_cash:.2f}%', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.88, f'GEOM AVG: {geom_mean_cash:.2f}%', transform=ax.transAxes, verticalalignment='top')

def _combined_outcome(ax, dice_outcomes, cash_outcomes, dice_to_cash_ratio):
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
    # Extract variable names for labels
    dice_name = extract_variable_name(dice_outcomes, globals())
    cash_name = extract_variable_name(cash_outcomes, globals())

    # Calculate the weighted average of the outcomes
    weighted_avg_outcomes = weighted_average(dice_outcomes, cash_outcomes, dice_to_cash_ratio)
    
    # Convert outcomes to percentage probabilities
    win_probabilities_weighted = [(outcome - 1.0) * 100 for outcome in weighted_avg_outcomes]

    # Convert outcomes to percentage categories for plotting
    categories_weighted = [str((outcome - 1) * 100) + "%" for outcome in weighted_avg_outcomes]

    # Plot the weighted average outcomes
    ax.plot(categories_weighted, win_probabilities_weighted, marker='^')

    # Set the y-axis limits
    ax.set_ylim([-50, 100])

    # Set the y-axis label
    ax.set_ylabel(f"{dice_to_cash_ratio[0] * 100} % " + dice_name + " and " + f"{dice_to_cash_ratio[1] * 100} % " + cash_name)

    # Enable the grid
    ax.grid(True)

    # Remove x-axis labels
    ax.set_xticks([])

    # Calculate the arithmetic and geometric mean of the dice outcomes
    arith_mean_combined = df_kelly.at['combined', 'arith_avg']
    geom_mean_combined = df_kelly.at['combined', 'geom_avg']

    cost = df_kelly.at['net/cost', 'arith_avg']
    net = df_kelly.at['net/cost', 'geom_avg']

    # Add annotations for arithmetic and geometric mean
    ax.text(0.02, 0.98, f'ARITHM AVG: {arith_mean_combined:.2f}%' + f' (Cost: {cost:.2f}%)', transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.88, f'GEOM AVG: {geom_mean_combined:.2f}%' + f' (Net: +{net:.2f}%)', transform=ax.transAxes, verticalalignment='top')


def kelly_criterion(dice_outcomes, cash_outcomes, dice_to_cash_ratio):
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
    _dice_outcome(ax2, dice_outcomes)

    # Subplot 3: Height of cash outcome
    _cash_outcome(ax3, dice_outcomes, cash_outcomes)

    # Subplot 4: Height of combined outcome
    _combined_outcome(ax4, dice_outcomes, cash_outcomes, dice_to_cash_ratio)

    # Adjust spacing between subplots
    plt.tight_layout()
    plt.show()
