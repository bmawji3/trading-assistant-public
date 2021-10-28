import os
import yfinance as yf


def gather_data(symbols_array, spaces_array):
    for space, arr in zip(spaces_array, symbols_array):
        data = yf.download(space, period='ytd', group_by='ticker')
        for symbol in arr:
            data[symbol].to_csv(f'{os.path.join(os.getcwd(), "data", f"{symbol}.csv")}')
