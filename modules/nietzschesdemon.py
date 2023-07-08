"""
"""

############
# IMPORTS #
############

import numpy as np

# Statistics
from scipy.stats.mstats import gmean
from scipy import stats

# Visualization
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
import seaborn as sns
import matplotlib.pyplot as plt


####################
# HELPER FUNCTIONS #
####################

def _dice_random_walk(num_walks, num_rolls, dice_outcomes):
    """
    Perform random walks based on weighted dice rolls.

    Arguments:
    - num_walks: Number of random walks to perform
    - num_rolls: Number of rolls per walk
    - dice_outcomes: Array of dice outcomes

    Returns:
    - walks: Array of random walks
    - percentiles: 5th, 50th (median) and 95th Percentiles of the random walks
    - median_walk: Median walk
    - median_return: Geometric mean of dice' chances
    - percentage_change: Percentage change from 1 for each walk
    """
    # Perform random walks
    walks = np.cumprod(np.random.choice(dice_outcomes, size=(num_walks, num_rolls)), axis=1)

    # Calculate percentiles
    percentiles = np.percentile(walks, [5, 50, 95], axis=0)
    median_walk = percentiles[1]

    # Calculate geometric mean for each walk
    geometric_means = np.power(walks[:, -1], 1 / num_rolls)
    median_return = (gmean(dice_outcomes) - 1) * 100

    # Calculate percentage change from 1
    percentage_change = (geometric_means - 1) * 100

    return walks, percentiles, median_walk, median_return, percentage_change

#############
# FUNCTIONS #
#############

def plot_random_walk_frequency_distribution(num_walks, num_rolls, dice_outcomes, title):
    """
    Plot random walks of weighted dice rolls.

    Arguments:
    - num_walks: Number of random walks to perform
    - num_rolls: Number of rolls per walk
    - dice_outcomes: Array of dice outcomes

    Returns:
    None
    """

    walks, percentiles, median_walk, median_return, percentage_change = _dice_random_walk(num_walks, num_rolls, dice_outcomes)

    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), gridspec_kw={'width_ratios': [2, 1]})

    # Plot random walks
    ax1.plot(range(num_rolls), walks.T, color='gray', alpha=0.3)

    # Plot 5th and 95th percentiles
    ax1.plot(range(num_rolls), percentiles[2], color='black', label='95th percentile')
    ax1.plot(range(num_rolls), percentiles[0], color='black', label='5th percentile')

    # Plot median walk
    ax1.plot(range(num_rolls), median_walk, color='red', label='Median')

    # Set axis labels and plot title
    ax1.set_xlabel('Rolls')
    ax1.set_ylabel('Ending Wealth')
    ax1.set_title(title)

    # Set logarithmic scale on the y-axis
    ax1.set_yscale('log')

    # Set the y-axis limits
    ax1.set_ylim([1e-12, 1e7])

    # Custom formatter for y-axis ticks
    def wealth_formatter(x, pos):
        if x >= 1:
            return f'{int(x):,}'
        else:
            return f'{float(x)}'

    formatter = FuncFormatter(wealth_formatter)
    ax1.yaxis.set_major_formatter(formatter)

    # Plot geometric mean and histogram
    ax2.axhline(median_return, color='red', linestyle='--', label='Geometric Mean')
    ax2.hist(percentage_change, bins=30, orientation='horizontal', color='grey', alpha=0.7)
    ax2.set_xlabel('Frequency')
    ax2.set_ylabel('Geometric Average Return')
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")

    # Set the y-axis limits
    ax2.set_ylim([-8, 4.5])

    # Adjust spacing between subplots
    plt.subplots_adjust(wspace=0.05)

    # Saving plot
    plt.savefig(f'../plots/random_walk_frequency_distribution_{median_return:.2f}.png', dpi=300)

    # Display the plot
    plt.show()

def plot_random_walk_geom_average(num_walks, num_rolls, Bet, title):
    """
    Plot random walks of weighted dice rolls.

    Arguments:
    - num_walks: Number of random walks to perform
    - num_rolls: Number of rolls per walk
    - bet: Instance of Bet object

    Returns:
    None
    """
    # Use dice_random_walk() to calculate the median_return and percentage_change.
    _, _, _, median_return, percentage_change = _dice_random_walk(num_walks, num_rolls, Bet.outcomes)

    # Create the plot
    fig, ax = plt.subplots(figsize=(5, 2))

    # Plot the geometric mean as a vertical line
    ax.axvline(median_return, color='red', linestyle='--', label='Median')

    # Create a KDE plot
    sns.kdeplot(percentage_change, color='black', linewidth=2, ax=ax)

    # Calculate 5th and 95th percentiles
    lower_bound, upper_bound = np.percentile(percentage_change, [5, 95])

    # Generate X values between lower and upper bound
    x = np.linspace(lower_bound, upper_bound, 100)

    # Get KDE for the generated X values
    kde = stats.gaussian_kde(percentage_change)
    y = kde(x)

    # Fill between the KDE plot and the X-axis between the lower and upper bound
    ax.fill_between(x, y, color='lightgrey', label='90% Interval')

    ax.set_xlabel('Geometric Average Return')
    ax.set_ylabel(title)

    # Set the x-axis limits
    ax.set_xlim([-8, 6])

    # Add legend
    ax.legend()

    # Create a formatter that displays y-values with three decimal places
    format_y = ticker.FuncFormatter(lambda x, pos: '{:.3f}'.format(x))
    
    # Apply the formatter to the y-axis
    ax.yaxis.set_major_formatter(format_y)

    # Saving plot
    plt.savefig(f'../plots/random_walk_geom_average_{median_return:.2f}.png', dpi=300)

    # Display the plot
    plt.show()
