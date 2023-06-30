import numpy as np
from scipy.stats.mstats import gmean

class Bet:
    """
    This class represents a bet, with a name, results, weights, and calulations for outcome, arithmetic mean, and geometric mean.
    """

    def __init__(self, name, results, weights):
        """
        Constructor of the Bet class.

        Parameters:
        name (str): The name of the bet.
        results (array): An array with 1 to 6 elements representing results of a dice roll
        weights (array): An array representing how often each result occurs. Each element must be an integer greater or equal to 1.


        
        Raises:
        AssertionError: If results and weights do not have the same length, or if results has not 1 to 6 elements, or if any element in weights is not an integer greater or equal to 1.
        """

        # Ensure that results and weights have the same length
        assert len(results) == len(weights), "Results and weights must have the same length."

        # Ensure that results has 1 to 6 elements
        assert len(results) >= 1 and len(results) <= 6, "Results must have 1 to 6 elements."

        # Ensure name is a string
        assert isinstance(name, str), "Name must be a string."

        # Ensure that all elements in weights are integers and are greater or equal to 1
        assert all(isinstance(i, int) and i >= 1 for i in weights), "All elements in weights must be integers greater or equal to 1."

        self.name = name.lower()
        self.results = np.array(results) 
        self.weights = np.array(weights) 
        
        # Calculation upon initialization
        self.outcomes = self.calculate_outcomes()
        self.arith_mean = self.calculate_arith_mean()
        self.geom_mean = self.calculate_geom_mean()

    def calculate_outcomes(self):
        """
        Iterates through the results and weights to give each dice site an outcome.

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

    def calculate_arith_mean(self):
        """
        Calculate the arithmetic mean of the outcome.
        
        Returns:
        float: The arithmetic mean of the outcome.
        """
        arith_mean = (np.mean(self.outcomes) - 1) * 100
        return arith_mean
    
    def calculate_geom_mean(self):
        """
        Calculate the geometric mean of the outcome.
        
        Returns:
        float: The geometric mean of the outcome.
        """
        geom_mean = (gmean(self.outcomes) - 1) * 100
        return geom_mean
    
class BetComparison:
    """
    This class represents a comparison between two Bet objects.
    """

    def __init__(self, bet1, bet2, ratio):
        """
        Constructor of the BetComparison class.

        Parameters:
        bet1 (Bet): The first bet to be compared.
        bet2 (Bet): The second bet to be compared.
        ratio (list): A list with exactly two elements that sum up to 1, representing the ratio of bet1 to bet2.
        
        Raises:
        AssertionError: If ratio does not have exactly two elements or does not sum up to 1.
        """

        # Ensure that bet1 and bet2 are both instances of the Bet class
        assert isinstance(bet1, Bet), "bet1 must be an instance of the Bet class."
        assert isinstance(bet2, Bet), "bet2 must be an instance of the Bet class."

        # Ensure that ratio has exactly two elements and sums up to 1
        assert len(ratio) == 2, "Ratio must have exactly two elements."
        assert np.isclose(sum(ratio), 1), "The elements of ratio must sum up to 1."

        self.bet1_name = bet1.name
        self.bet2_name = bet2.name
        self.__dict__[self.bet1_name] = bet1
        self.__dict__[self.bet2_name] = bet2
        self.ratio = ratio
        self.arith_mean_combined, self.geom_mean_combined, self.cost, self.net, self.results = self.weighted_average()

    def weighted_average(self):
        """
        Calculate arithmetic mean of a combined wager of dice and cash.
        
        Args:
        dice_outcomes (array-like): Dice outcomes
        cash_outcomes (array-like): Cash outcomes
        dice_to_cash_ratio (array-like): Ratio of dice to cash
        
        Returns:
        dict: Dictionary containing the calculated arithmetic means
        """
        
        # Combine the outcomes based on the given ratio and calculate the arithmetic mean
        results = self.ratio[0] * self.__dict__[self.bet1_name].outcomes + self.ratio[1] * self.__dict__[self.bet2_name].outcomes
        
        # Calculate the arithmetic/geometric mean of the combined outcomes
        arith_mean_combined = (np.mean(results) - 1) * 100
        geom_mean_combined = (gmean(results) - 1) * 100
        
        # Calculate the cost
        cost = arith_mean_combined - self.__dict__[self.bet1_name].arith_mean - self.__dict__[self.bet2_name].arith_mean
        net = geom_mean_combined - self.__dict__[self.bet1_name].geom_mean - self.__dict__[self.bet2_name].geom_mean
        
        return arith_mean_combined, geom_mean_combined, cost, net, results