import pandas as pd
import os

def get_wsb_volume_for_date(symbol, given_date):
    # gather reddit mention counts
    # This allows for relative path retrieval for WebApp and WebAPI
    reddit_fp = os.path.join('trading_assistant_app', 'reddit_refined', f'{symbol}_rss_wc.csv')

    # This should be used when running the app/main function independent of WebApp and WebAPI
    # reddit_fp = os.path.join(os.getcwd(), 'reddit_data', f'{symbol}_rss_wc.csv')

    try:
        df_reddit = pd.read_csv(reddit_fp)
    except FileNotFoundError as e:
        return {
            'wsb_volume': 0
        }

    df_reddit = df_reddit.set_index('Date')
    df_reddit.index = pd.to_datetime(df_reddit.index)
    df_reddit = df_reddit.drop('Ticker', axis=1)

    try:
        value = df_reddit['wsb_volume'][given_date].item()
        return_dict = {
            'wsb_volume': value
        }
    except KeyError as e:
        # print(f'Invalid given_date index/key for {e}')
        return_dict = {
            'wsb_volume': 0
        }

    return return_dict
def get(ticker_id):
    ## Returns dictionary of stock data
    data = pd.read_csv(f'trading_assistant_app/data/{ticker_id}.csv')  # read CSV
    reddit = pd.read_csv(f'trading_assistant_app/reddit_refined/{ticker_id}_rss_wc.csv')
    reddit = reddit[["Date", "wsb_volume"]]
    data = data.merge(reddit, how='left', on='Date')
    data['wsb_volume'] = data['wsb_volume'].fillna(0)
    return data.to_dict()  # convert dataframe to dictionary


test = get("AAL")

r = 1