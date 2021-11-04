import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
from datetime import date
today = date.today()

def import_function():
    stock_csv = pd.read_csv("sp500.csv")
    stock_list = stock_csv.Symbol
    #stock_list = stock_list[:5] #Testing first six

    for i in stock_list:
        yf.pdr_override()
        data1 = pdr.get_data_yahoo(i, start="2011-11-01", end=today)
        filename = "./data/" + i + ".csv"
        data1.to_csv(filename)

def test_code():
    import_function()

if __name__ == "__main__":
    test_code()