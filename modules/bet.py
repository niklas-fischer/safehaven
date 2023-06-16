import numpy as np

class Bet:
    """
    This class represents a bet, with a name, results, weights, and an outcome.
    """

    def __init__(self, name, results, weights):
        """
        Constructor of the Bet class.

        Parameters:
        name (str): The name of the bet.
        results (list): A list with 1 to 6 elements representing results.
        weights (list): A list with equal number of elements as results representing the weights. Each element must be an integer greater or equal to 1.

        Raises:
        AssertionError: If results and weights do not have the same length, or if results has not 1 to 6 elements, or if any element in weights is not an integer greater or equal to 1.
        """

        # Ensure that results and weights have the same length
        assert len(results) == len(weights), "Results and weights must have the same length."

        # Ensure that results has 1 to 6 elements
        assert len(results) >= 1 and len(results) <= 6, "Results must have 1 to 6 elements."

        # Ensure that all elements in weights are integers and are greater or equal to 1
        assert all(isinstance(i, int) and i >= 1 for i in weights), "All elements in weights must be integers greater or equal to 1."

        self.name = name
        self.results = np.array(results)
        self.weights = np.array(weights)

        # Calculate the outcome upon initialization
        self.outcomes = self.calculate_outcomes()

    def calculate_outcomes(self):
        """
        Calculate the outcome by repeating each element in results as many times as the corresponding weight.
        The outcome is stored as a numpy array.

        Returns:
        np.array: The outcome as a numpy array.
        """

        outcomes = np.array([])
        for i in range(len(self.weights)):
            # Repeat each element in results as many times as the corresponding weight
            repeated_values = np.repeat(self.results[i], self.weights[i])
            
            # Add the repeated values to the outcome
            outcomes = np.concatenate((outcomes, repeated_values))
        return outcomes
