"""

"""

###########
# IMPORTS #
###########
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter 
import pandas as pd


####################
# HELPER FUNCTIONS #
####################

def _plot_sp500(ax, sp500, safe_haven, categories):
    """
    Plotting S&P 500 data distribution in given categories bins.
    """
    
    # Set the category order for the ReturnRange column
    sp500['ReturnRange'] = sp500['ReturnRange'].astype(pd.CategoricalDtype(categories=categories, ordered=True))
    
    # Create yearly returns of S&P 500 plot
    sns.countplot(x='ReturnRange', data=sp500, color='#3a89bf', ax=ax)
    
    # Set axis labels and titles
    ax.set_ylabel('SPX Distribution')
    ax.set_title(safe_haven['title'])
    
    # Show percentage symbol on y-axis as integers
    ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))
    
    # Move xticks to top
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')  # Move x-axis label to top
    
    # Adjust X-axis labels
    ax.set_xticklabels(categories, rotation=45)
    ax.set_xlabel('')

def _plot_return_ranges(ax, sp500, marker):
    """
    Plots a bar chart of total returns of S&P 500 on a specified axis.

    Parameters:
    ax: The axis (subplot) on which the function should draw
    sp500 (DataFrame): The input DataFrame containing 'TotalReturn' and 'ReturnRange' columns (data of S&P 500)
    marker: Marker symbol
    """

    # Grouping and Aggregating by `ReturnRange`
    grouped = sp500.groupby('ReturnRange')['TotalReturn'].agg(['min', 'max', 'mean'])

    # Sorting by mean
    grouped = grouped.sort_values(by='mean')

    # Using 'min' as bottom, adjust the height of 'max' by the difference between 'max' and 'min'
    bars = ax.bar(grouped.index, grouped['max'] - grouped['min'], bottom=grouped['min'], color='#3a89bf')

    # Set Y-axis limits
    ax.set_ylim(-0.5, 1.0)  # -50% to 100%

    # Remove X-axis labels
    ax.set_xticks([])

    # Add a black line at 0%
    ax.axhline(0, color='lightgrey', linewidth=0.8)

    # Format Y-axis labels as percentages
    def percent(x, pos):
        return f"{x:.0%}"

    # Format Y-axis labels as percentages
    ax.yaxis.set_major_formatter(FuncFormatter(percent))

    # Mark average returns with 'x' in blue
    ax.scatter(grouped.index, grouped['mean'], color='black', marker=marker, s=40)

    # Connect average returns with dashed blue line
    ax.plot(grouped.index, grouped['mean'], color='black', linestyle='--')
    
    # Set plot label
    ax.set_ylabel('SPX')

def _plot_safe_haven(ax, safe_haven, categories, marker):
    """Plot the outcomes for a given store of value on a specified axis."""
    min_val, max_val = min(safe_haven["outcomes"]), max(safe_haven["outcomes"])

    # Adjust y-axis
    if min_val < 0 or max_val > 0.20:
        ax.set_ylim(min_val - 0.5, max_val + 0.5)  # 5% buffer on both ends
    else:
        ax.set_ylim(0, 0.25)

    # Seaborn Lineplot
    sns.lineplot(x=categories, y=safe_haven["outcomes"], marker=marker, linewidth=1, markersize=8, color='black', ax=ax)

    # Additional plot adjustments
    ax.set_xticks([])  # Remove x-axis ticks
    ax.grid(axis='y', linestyle='--', alpha=0.7)  # Add horizontal grid lines
    ax.set_ylabel(safe_haven["title"])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))  # Format y-axis as percentage


def _plot_combined_outcome(ax, sp500, safe_haven, weights):
    """
    Plots a line chart of a weighted outcome of the S&P 500 and a safe haven prototype.

    Parameters:
    ax: Plotting axis
    sp500 (DataFrame): The input DataFrame containing 'TotalReturn' and 'ReturnRange' columns (data of S&P 500)
    safe_haven (dict): Contains outcomes as an array and a title
    weights (list): List of two weights for S&P 500 and safe haven respectively

    Returns:
    None (displays the plot)
    """    
    # Grouping and Aggregating by `ReturnRange`, getting min and max data points:
    grouped = sp500.groupby('ReturnRange')['TotalReturn'].agg(['min', 'max', 'mean'])

    grouped = grouped.sort_values(by='mean')

    bars = ax.bar(grouped.index, grouped['max'] - grouped['min'], bottom=grouped['min'], color='#3a89bf', label="Return Range")

    # Ensure the safe_haven outcomes and the DataFrame have the same length
    if len(grouped) != len(safe_haven['outcomes']):
        raise ValueError("Length of safe_haven outcomes does not match DataFrame group length.")

    # Calculate the weighted average
    weighted_average = (grouped['mean'] * weights[0] + safe_haven['outcomes'] * weights[1]) / sum(weights)

    # Set Y-axis limits
    ax.set_ylim(-0.5, 1.0)  # -50% to 100%

    # Remove X-axis labels
    ax.set_xticks([])

    # Add a black line at 0%
    ax.axhline(0, color='black', linewidth=0.8)

    # Format Y-axis labels as percentages
    def percent_formatter(x, pos):
        return f"{x:.0%}"
    
    ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

    # Plot the weighted average returns with dashed black line
    ax.plot(grouped.index, weighted_average, color='black', linestyle='--')

    # Mark average returns with 'x' in blue
    ax.scatter(grouped.index, weighted_average, color='black', marker='^', s=40)
    
    # Set plot label
    ax.set_ylabel(f"{weights[0] * 100} % SPX &\n {weights[1] * 100} % {safe_haven['title']}")

############# 
# FUNCTIONS #
#############

def percent_formatter(x, pos):
    return f"{x/100:.0%}"

######### 
# PLOTS #
#########

def plot_xo_sp500(sp500, safe_haven, weights):
    """
    This function calculates the outcome of a weighted comparison of the S&P500 with different type of safe havens

    Arguments:
    - sp500: A DataFrame with data from S&P 500, calculated with package sp500.py
    - safe_haven: A possible safe haven 
    - weights: A numpy array with two elements representing the weights for S&P 500 data and possible safe haven

    Return:
    None
    """
    # Manually define the order of the categories
    categories = ['< -15%', '-15% to 0%', '0% to 15%', '15% to 30%', '> 30%']

    # Create a figure with 4 subplots
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(3, 8))

    # Subplot 1: Distribution of S&P 500 outcomes
    _plot_sp500(ax1, sp500, safe_haven, categories)

    # Subplot 2: S&P 500 return ranges
    _plot_return_ranges(ax2, sp500, 'x')

    # Subplot 3: Plot safe haven cartoon outcome
    _plot_safe_haven(ax3, safe_haven, categories, 'o')

    # Subplot 4: Combined safe haven cartoon prototype outcome
    _plot_combined_outcome(ax4, sp500, safe_haven, weights)

    # Adjust spacing between subplots
    plt.tight_layout()

    # Saving plot
    plt.savefig(f"../plots/xo_sp500_{safe_haven['title']}.png", dpi=300)
