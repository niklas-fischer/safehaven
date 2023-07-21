import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter

class DataProcessor:
    """
    Class to handle data processing tasks such as checking the size of input data and calculating its minimum and maximum values.
    """
    def __init__(self, data):
        """
        Initialize with data array.
        """
        self.data = data

    def check_size(self):
        """
        Ensures that the input data array has exactly 5 elements. Throws an assertion error if this condition is not met.
        """
        assert len(self.data) == 5, "The input array should contain exactly 5 values."

    def calculate_min_max(self):
        """
        Calculates minimum and maximum values for the input data array. Adjusts these values according to the specified conditions.
        Returns the minimum and maximum values.
        """
        min_value = np.min(self.data)
        max_value = np.max(self.data)

        # Check conditions and adjust min_value and max_value if needed
        if min_value >= 0:
            min_value = 0
        else:
            min_value = min_value - 1

        if max_value < 0.25:
            max_value = 0.25
        else:
            max_value = max_value + 1

        return min_value, max_value

class PlotPrototype:
    """
    Class to handle plotting tasks such as creating a line graph with points for the given percentage values.
    """
    def __init__(self, data, categories, title, xlabel="SPX Returns"):
        """
        Initialize with data array, categories, title, and x-axis label.
        """
        self.data = data
        self.categories = categories
        self.title = title
        self.xlabel = xlabel

    def plot_spx_prototype_payoff(self, min_value, max_value):
        """
        Plots a line graph  for SPX prototype payoffs with points for the 
        given percentage values.
        The x-axis represents categories and the y-axis represents percentage returns.
        """
        fig, ax = plt.subplots(figsize=(3,2))
        ax.plot(self.categories, self.data, 'o-', markerfacecolor="None")

        # Rotate x-axis labels
        plt.xticks(rotation=45)
        # Set y-axis limits
        ax.set_ylim([min_value, max_value])

        # Set y-axis tick values and labels
        vals = ax.get_yticks()
        ax.yaxis.set_major_locator(FixedLocator(vals))
        ax.yaxis.set_major_formatter(FixedFormatter(['{:,.0%}'.format(x) for x in vals]))

        # Set title and x-axis label
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)

        plt.show()