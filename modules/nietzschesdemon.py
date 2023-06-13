"""
"""

############
# IMPORTS #
############

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import gmean
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter

##############
# FUNCTIIONS #
##############

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

def plot_random_walk_frequency_distribution(num_walks, num_rolls, dice_outcomes):
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [2, 1]})

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
    ax1.set_title('You Get What You Get, Not What You Expect')

    # Set logarithmic scale on the y-axis
    ax1.set_yscale('log')

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

    # Adjust spacing between subplots
    plt.subplots_adjust(wspace=0.05)

    # Saving plot
    plt.savefig('../plots/random_walk_frequency_distribution.png', dpi=300)

    # Display the plot
    plt.show()

def plot_random_walk_geom_average(num_walks, num_rolls, dice_outcomes):
    """
    Plot random walks of weighted dice rolls.

    Arguments:
    - num_walks: Number of random walks to perform
    - num_rolls: Number of rolls per walk
    - dice_outcomes: Array of dice outcomes

    Returns:
    None
    """
    # Use dice_random_walk() to calculate the median_return and percentage_change.
    _, _, _, median_return, percentage_change = _dice_random_walk(num_walks, num_rolls, dice_outcomes)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot the geometric mean as a vertical line
    ax.axvline(median_return, color='red', linestyle='--', label='Geometric Mean')

    # Plot the histogram of percentage_change
    bins = np.linspace(np.min(percentage_change), np.max(percentage_change), 30)
    counts, bins, _ = ax.hist(percentage_change, bins=bins, orientation='vertical', color='lightgrey', alpha=0.7)
    mid_points = (bins[:-1] + bins[1:]) / 2
    ax.plot(mid_points, counts, color='black', linewidth=2)

    ax.set_xlabel('Geometric Average Return')
    ax.set_ylabel('Frequency')

    # Saving plot
    plt.savefig('../plots/random_walk_geom_average.png', dpi=300)

    # Display the plot
    plt.show()
