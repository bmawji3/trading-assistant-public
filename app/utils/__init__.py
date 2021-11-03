import datetime as dt
import pandas as pd
import data_util as util
import indicators as ta


if __name__ == '__main__':
    # main()
    symbols = ["FB", "AAPL"]
    start_date = dt.datetime(2021, 1, 15)
    end_date = dt.datetime(2021, 4, 27)
    dates = pd.date_range(start_date,end_date)

    # prices_df = util.get_closings(symbols, dates)
    # prices_normed = util.normalize(prices_df)
    # plot_data(prices_normed)

    FB_stock_data = util.get_ohlcv("FB", dates)
    # print(FB_stock_data)

    # sma_FB = ta.sma(FB_stock_data,window=5)
    # print(sma_FB.columns)
    
    # ema_FB = ta.ema(FB_stock_data,window=5)
    # print(ema_FB)

    vama_FB = ta.vama(FB_stock_data,window=5)
    print(vama_FB)