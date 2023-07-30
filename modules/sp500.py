import pandas as pd
import quandl
import seaborn as sns
import matplotlib.pyplot as plt

class DataLoader:
    """
    This class is responsible for loading data from Quandl and storing them in a DataFrame
    """

    def __init__(self, start_date, end_date, price_code, yield_code):
        self.start_date = start_date
        self.end_date = end_date
        self.price_code = price_code
        self.yield_code = yield_code

    def load_data(self):
        """
        Load data from Quandl
        """
        # Loading S&P 500 yearly return and dividend data
        df_price = quandl.get(self.price_code, start_date=self.start_date, end_date=self.end_date)
        df_yield = quandl.get(self.yield_code, start_date=self.start_date, end_date=self.end_date)
        return df_price, df_yield


class DataProcessor:
    """
    This class is responsible for processing loaded data.
    """

    def process_data(self, df_price, df_yield):
        """
        Processing `df_price` and `df_yield` to calculate return of SPX in last 120 years
        """
        # Setting date range for df_price (data from first of year)
        df_price = df_price[df_price.index.month == 1]
        df_price = df_price[df_price.index.day == 1]
        
        # Setting date range for df_yield (data from end of year)
        df_yield = df_yield[df_yield.index.month == 12]
        df_yield = df_yield[df_yield.index.day == 31]
        
        # Add one day to have equivalent year indices
        df_yield.index = df_yield.index + pd.Timedelta(days=1)

        # Change `DividendYield` to percentage
        df_yield['DividendYield'] = df_yield['Value'] / 100

        # Drop `Value` column
        df_yield = df_yield.drop(columns='Value')
        
        # Add new column `Return` by calculing percentage change in `Value`
        df_price['Return'] = df_price['Value'].pct_change()

        # Join `df_price` and `df_yield` on index
        df_merged = df_price.join(df_yield, how='inner')
        
        # Add new column `TotalReturn` by summing return and dividend yield
        df_merged['TotalReturn'] = df_merged['Return'] + df_merged['DividendYield']

        # Setting bin edges and labels
        bin_edges = [-float('inf'),-0.15,0,0.15,0.3,float('inf')]
        bin_labels = ['< -15%', '-15% to 0%', '0% to 15%', '15% to 30%', '> 30%']
        
        # Adding new column `ReturnRange` by bins set
        df_merged['ReturnRange'] = pd.cut(df_merged['TotalReturn'], bin_edges, labels=bin_labels)
        
        return df_merged


class DataSaver:
    """
    This class is responsible for saving processed data to a CSV file.
    """

    def save_data_to_csv(self, df, path, sep=';'):
        """
        Saving DataFrame to csv
        """
        df.to_csv(path, sep=sep)


class DataVisualizer:
    """
    This class is responsible for visualizing processed SP500 data.
    """

    def plot_data(self, df, start_date, end_date):
        """
        Plotting DataFrame with SNS
        """
        # Create yearly returns of S&P 500 plot
        sns.countplot(x='ReturnRange', data=df, color='#3a89bf')
        
        # Set axis labels and titles
        plt.xlabel('Yearly Return')
        plt.ylabel('Frequency')
        plt.title('Frequency Distribution of SPX Annual Returns, ' + start_date.strftime('%Y') + '-' + end_date.strftime('%Y'))
        plt.show()
