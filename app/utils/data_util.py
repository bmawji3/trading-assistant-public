import os
from pandas.core.frame import DataFrame
import yfinance as yf
import pandas as pd
from pandas import DatetimeIndex
import matplotlib.pyplot as plt


def gather_data(symbols_array, spaces_array):
    for space, arr in zip(spaces_array, symbols_array):
        data = yf.download(space, period='ytd', group_by='ticker')
        for symbol in arr:
            data[symbol].to_csv(f'{os.path.join(os.getcwd(), "data", f"{symbol}.csv")}')


def symbol_to_path(symbol: str, base_dir: str = None) -> str:
    """Return CSV file path given ticker symbol.
    :param symbol: ticker symbol
    :param base_dir: relative location of market data folder
    :return: relative location of CSV file
    """

    if base_dir is None:
        base_dir = os.environ.get("MARKET_DATA_DIR", "../data/")
    return os.path.join(base_dir, "{}.csv".format(symbol))


def get_prices(symbols: list, dates: DatetimeIndex, adj_close_col_name: str ="Adj Close") -> DataFrame:
    """Read stock data (adjusted close) for given symbols from downloaded CSV files.
    :param symbols: list of symbols to read from CSV files
    :param dates: dates for the data retrieval
    # :param addSPY: whether to add SPY to the columns
    :param adj_close_col_name: column name to retrieve adjusted closing prices
    :type symbols: list
    """

    prices = pd.DataFrame(index=dates)

    if "SPY" not in symbols:  # add SPY for reference, if absent  		  	   		   	 		  		  		    	 		 		   		 		  
        symbols_addSPY = ["SPY"] + list(symbols)  # handles the case where symbols is np array of 'object' 

    if symbols == []:
        symbols_addSPY = ["SPY"]

    for symbol in symbols_addSPY:
        df_temp = pd.read_csv(
            symbol_to_path(symbol),
            index_col="Date",
            parse_dates=True,
            usecols=["Date", adj_close_col_name],
            na_values=["nan"],
        )
        df_temp = df_temp.rename(columns={adj_close_col_name: symbol})
        prices = prices.join(df_temp)
        if symbol == "SPY":  # drop dates when SPY did not trade  		  	   		   	 		  		  		    	 		 		   		 		  
            prices = prices.dropna(subset=["SPY"])

    if "SPY" not in symbols and symbols != []:
        prices = prices.drop("SPY", axis=1)  # remove SPY as it was only needed for trading days
    
    prices.ffill(inplace=True)  # first forward fill prices
    prices.bfill(inplace=True)  # second backward fill prices

    return prices

def clean_data(symbol: str, dates: DatetimeIndex) -> DataFrame:
    """Ensures stock data match days where SPY traded and fills any missing data.
    :param symbol: Stock symbol
    :param dates: Dates of stock data to clean
    """
    SPY_adj_close = get_prices(symbols=[],dates=dates)
    

    symbol_data = pd.read_csv(symbol_to_path(symbol), index_col="Date", parse_dates=True, na_values=["nan"])
    stock_data = pd.merge(SPY_adj_close, symbol_data, how="inner", left_index=True, right_index=True)
    stock_data = stock_data.drop("SPY", axis=1)
    stock_data.ffill(inplace=True)
    stock_data.bfill(inplace=True)

    return stock_data

def normalize_prices(prices: DataFrame) -> DataFrame:
    """Normalize the prices
    :param prices: DataFrame of closing prices
    """
    return prices/prices.iloc[0]


def plot_data(prices: DataFrame, title: str = "Stock prices", xlabel:str = "Date", ylabel: str = "Price" ) -> None:	 		  		  		    	 		 		   		 		  
    """Plot stock prices with a custom title and meaningful axis labels."""	  	   		   	 		  		  		    	 		 		   		 		  
    ax = prices.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)  		  	   		   	 		  		  		    	 		 		   		 		  
    ax.set_ylabel(ylabel)  		  	   		   	 		  		  		    	 		 		   		 		  
    plt.show()
