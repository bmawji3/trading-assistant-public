import datetime as dt
import pandas as pd
import data_util as util

if __name__ == '__main__':
    # main()
    symbols = ["FB", "AAPL"]
    start_date = dt.datetime(2021, 1, 15)
    end_date = dt.datetime(2021, 4, 27)
    dates = pd.date_range(start_date,end_date)

    prices_df = util.get_prices(symbols, dates)
    prices_normed = util.normalize_prices(prices_df)
    # plot_data(prices_normed)

    FB_stock_data = util.clean_data("FB", dates)
    # print(FB_stock_data)