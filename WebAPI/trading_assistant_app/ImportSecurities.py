import os
import pandas as pd
import yfinance as yf

from pandas_datareader import data as pdr
from datetime import date
today = date.today()


def import_function(reddit_list=None):
    if reddit_list is None:
        reddit_list = list()

    if len(reddit_list) == 0:
        stock_csv = pd.read_csv(os.path.join("trading_assistant_app", "sp500.csv"))
        stock_list = stock_csv.Symbol
    else:
        stock_list = reddit_list
    #stock_list = stock_list[:5] #Testing first six

    for i in stock_list:
        yf.pdr_override()
        data1 = pdr.get_data_yahoo(i, start="2011-11-01", end=today)
        filename = "./trading_assistant_app/data/" + i + ".csv"
        data1.to_csv(filename)


def test_code():
    import_function()


if __name__ == "__main__":
    test_code()
