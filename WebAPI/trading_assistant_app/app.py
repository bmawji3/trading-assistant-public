import datetime as dt
import json
import os
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

# Statements with "." allows for relative path importing for WebApp and WebAPI
from .ImportSecurities import *
from .utils.aws_util import *
from .utils.data_util import *
from .utils.indicators import *

# Statements without "." should be used when running the app/main function independent of WebApp and WebAPI
# from ImportSecurities import *
# from utils.aws_util import *
# from utils.data_util import *
# from utils.indicators import *


def prepare_data(symbols, start_date, end_date, percent_gain, debug=False):
    # df_array = list()

    # initialize dictionary to hold dataframe per symbol
    df_dict = {}

    # remove the index from the list of symbols
    if "SPY" in symbols:
        symbols.remove("SPY")

    for symbol in symbols:
        # get stock data for a given time

        # This allows for relative path retrieval for WebApp and WebAPI
        stock_data = get_ohlcv(symbol, start_date, end_date, base_dir=os.path.join('trading_assistant_app', 'data'))

        # This should be used when running the app/main function independent of WebApp and WebAPI
        # stock_data = get_ohlcv(symbol, start_date, end_date, base_dir=os.path.join(os.getcwd(), 'data'))

        # Filter out empty OHLCV DF
        if len(stock_data) == 0:
            continue

        # calculate technical indicators
        df_indicators = get_technical_indicators_for_symbol(stock_data)

        # gather reddit mention counts
        # This allows for relative path retrieval for WebApp and WebAPI
        reddit_fp = os.path.join('trading_assistant_app', 'reddit_data', f'{symbol}_rss.csv')

        # This should be used when running the app/main function independent of WebApp and WebAPI
        # reddit_fp = os.path.join(os.getcwd(), 'reddit_data', f'{symbol}_rss.csv')

        df_reddit = pd.read_csv(reddit_fp)
        df_reddit = df_reddit.set_index('Date')
        df_reddit.index = pd.to_datetime(df_reddit.index)
        df_reddit = df_reddit.drop('Ticker', axis=1)

        # merge and fill nan data
        df_merged = pd.merge(df_indicators, df_reddit, how='left', left_index=True, right_index=True)
        df_merged[['wsb_volume']] = df_merged[['wsb_volume']].fillna(value=0.0)

        # initialize dataframe to hold indicators and signal
        df = df_merged.copy(deep=True)

        # extract closing prices
        prices = stock_data["close"]

        # initialize signal
        signal = prices * 0

        # target holding period to realize gain
        holding_period = 5

        # buy signal == 1 when price increases by percent_gain and sell == -1 when it decreases by percent_gain
        for i in range(prices.shape[0] - holding_period):
            ret = (prices.iloc[i + 5] / prices.iloc[i]) - 1
            if ret > percent_gain:
                signal.iloc[i] = 1
            elif ret < (-1 * percent_gain):
                signal.iloc[i] = -1
            else:
                signal.iloc[i] = 0

        df["signal"] = signal.values
        df_dict[symbol] = df

        if debug:
            print(stock_data.head(n=20), '\n')
            print(df_indicators.head(n=20), '\n')
            print(df_indicators.columns)
            print(df_indicators.head(n=20), '\n')

    return df_dict


def train_model(df, symbol, debug=False):
    feature_cols = df.columns[:-1]
    label_cols = df.columns[-1:]
    train, test = np.split(df, [int(.6 * len(df))])
    X_train, y_train = train[feature_cols], train[label_cols]
    X_test, y_test = test[feature_cols], test[label_cols]

    # print('X_train\n', X_train.head(20))
    # print('y_train\n', y_train.head(20))
    # print('X_test\n', X_test.head(20))
    # print('y_test\n', y_test.head(20))

    clf = RandomForestClassifier(n_estimators=10, random_state=42)
    # Workaround to get data with NAN/INF working
    if np.any(np.isnan(X_train)) == False and \
            np.all(np.isfinite(X_train)) == True and \
            np.any(np.isnan(y_train.values.ravel())) == False and \
            np.all(np.isfinite(y_train.values.ravel())) == True:
        clf.fit(X_train, y_train.values.ravel())
        y_pred = clf.predict(X_test)
        y_test_ravel = y_test.values.ravel()
        df_y_pred = pd.DataFrame(y_pred, index=y_test.index, columns=[f'Y_{symbol}'])

        if debug:
            print(f'Feature Importances: '
                  f'{sorted(list(zip(X_train, clf.feature_importances_)), key=lambda tup: tup[1], reverse=True)}')
            print(f'Mean Absolute Error: {metrics.mean_absolute_error(y_test_ravel, y_pred)}')
            print(f'Mean Squared Error: {metrics.mean_squared_error(y_test_ravel, y_pred)}')
            print(f'Root Mean Squared Error: {np.sqrt(metrics.mean_squared_error(y_test_ravel, y_pred))}')
    else:
        df_y_pred = pd.DataFrame(np.zeros(len(y_test)), index=y_test.index, columns=[f'Y_{symbol}'])

    return df_y_pred


def s3_upload_and_list():
    # Set up variables
    cwd = os.getcwd()
    data_directory = os.path.join(cwd, 'data')

    # Read Config
    aws_config_fp = os.path.join(os.getcwd(), 'config', 'aws_config.json')
    with open(aws_config_fp) as fp:
        aws_config = json.load(fp)

    # Set up Session & Resource
    session = start_session(aws_config['access_key'], aws_config['secret_access_key'])
    s3 = get_s3_resource(session)
    bucket = aws_config['bucket_name']

    # List current Buckets & Objects per Bucket
    print_bucket_objects(s3, bucket)

    # Upload files to Bucket
    files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]
    for file in files:
        upload_file_to_bucket(s3, bucket, os.path.join(data_directory, file), file)

    # (Optional) Delete files from Bucket
    # for file in files:
    #     delete_object(s3, bucket, file)

    # List Buckets & Objects after Upload
    print_bucket_objects(s3, bucket)


def gather_download_data(sd, ed, download_new_data=False):
    symbols_config_fp = os.path.join(os.getcwd(), 'config', 'symbols_config.json')
    with open(symbols_config_fp) as fp:
        symbols_config = json.load(fp)

    symbols_array = []
    for category, array in symbols_config.items():
        symbols_array.append(array)
    flat_symbols = [item for sublist in symbols_array for item in sublist]

    if download_new_data:
        spaces_array = []
        for array in symbols_array:
            spaces = " ".join(array)
            spaces_array.append(spaces)
        gather_data(symbols_array, spaces_array, sd=sd, ed=ed)


def get_list_of_predicted_stocks(percent_gain, given_date, debug=False):
    buy_signal_recognized_list = list()
    sell_signal_recognized_list = list()
    empty_df_count = 0
    cwd = os.getcwd()

    # This allows for relative path retrieval for WebApp and WebAPI
    data_directory = os.path.join(cwd, 'trading_assistant_app', 'data')

    # This should be used when running the app/main function independent of WebApp and WebAPI
    # data_directory = os.path.join(cwd, 'data')

    files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]
    symbols = [symbol.split('.csv')[0] for symbol in files]
    start_date = dt.datetime(2011, 11, 1)
    end_date = dt.date.today()
    df_dictionary = prepare_data(symbols=symbols, start_date=start_date, end_date=end_date, percent_gain=percent_gain)

    for symbol, df in df_dictionary.items():
        if len(df) == 0:
            print(f'len(df) == 0!!! for {symbol}')
            empty_df_count += 1
            continue

        # Train model
        df_prediction = train_model(df, symbol, debug=debug)
        try:
            if df_prediction[f'Y_{symbol}'][given_date] == 1:
                buy_signal_recognized_list.append(symbol)
            elif df_prediction[f'Y_{symbol}'][given_date] == -1:
                sell_signal_recognized_list.append(symbol)
        except KeyError as e:
            # print(f'Invalid given_date index/key for {e}')
            pass

    return {
        'buy_signal_recognized_list': buy_signal_recognized_list,
        'len_buy_signal_list': len(buy_signal_recognized_list),
        'sell_signal_recognized_list': sell_signal_recognized_list,
        'len_sell_signal_list': len(sell_signal_recognized_list),
        'len_files': len(files),
        'empty_df_count': empty_df_count,
        'given_date': given_date
    }


def get_technical_indicators_for_date(symbol,
                                      given_date,
                                      start_date=dt.datetime(2011, 11, 1),
                                      end_date=dt.datetime.today()):
    stock_data = get_ohlcv(symbol, start_date, end_date, base_dir='trading_assistant_app/data')
    technical_indicators = get_technical_indicators_for_symbol(stock_data)

    try:
        return_dict = {
            'Price/SMA5': technical_indicators['Price/SMA5'][given_date],
            'Price/SMA10': technical_indicators['Price/SMA10'][given_date],
            'Price/SMA20': technical_indicators['Price/SMA20'][given_date],
            'Price/SMA50': technical_indicators['Price/SMA50'][given_date],
            'Price/SMA200': technical_indicators['Price/SMA200'][given_date],
            'BB%10': technical_indicators['BB%10'][given_date],
            'BB%20': technical_indicators['BB%20'][given_date],
            'BB%50': technical_indicators['BB%50'][given_date],
            'RSI5': technical_indicators['RSI5'][given_date],
            'RSI10': technical_indicators['RSI10'][given_date],
            'MACD9': technical_indicators['MACD9'][given_date],
            'MOM5': technical_indicators['MOM5'][given_date],
            'VAMA10': technical_indicators['VAMA10'][given_date]
        }
    except KeyError as e:
        print(f'Invalid given_date index/key for {e}')
        return_dict = {
            'Price/SMA5': 0,
            'Price/SMA10': 0,
            'Price/SMA20': 0,
            'Price/SMA50': 0,
            'Price/SMA200': 0,
            'BB%10': 0,
            'BB%20': 0,
            'BB%50': 0,
            'RSI5': 0,
            'RSI10': 0,
            'MACD9': 0,
            'MOM5': 0,
            'VAMA10': 0
        }

    return return_dict


def get_wsb_volume_for_date(symbol, given_date):
    # gather reddit mention counts
    # This allows for relative path retrieval for WebApp and WebAPI
    reddit_fp = os.path.join('trading_assistant_app', 'reddit_data', f'{symbol}_rss.csv')

    # This should be used when running the app/main function independent of WebApp and WebAPI
    # reddit_fp = os.path.join(os.getcwd(), 'reddit_data', f'{symbol}_rss.csv')

    df_reddit = pd.read_csv(reddit_fp)
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


def get_technical_indicators_for_symbol(stock_data):
    price_sma_5_symbol = get_price_sma(stock_data, window=5)
    price_sma_10_symbol = get_price_sma(stock_data, window=10)
    price_sma_20_symbol = get_price_sma(stock_data, window=20)
    price_sma_50_symbol = get_price_sma(stock_data, window=50)
    price_sma_200_symbol = get_price_sma(stock_data, window=200)
    bb10_pct_symbol = get_bb_pct(stock_data, window=10)
    bb20_pct_symbol = get_bb_pct(stock_data, window=20)
    bb50_pct_symbol = get_bb_pct(stock_data, window=50)
    rsi5_symbol = get_rsi(stock_data, window=5)
    rsi10_symbol = get_rsi(stock_data, window=10)
    macd_symbol = get_macd_signal(stock_data, signal_days=9)
    mom_symbol = get_momentum(stock_data, window=5)
    vama_symbol = get_vama(stock_data, window=10)

    # Compile TA into joined DF & FFILL / BFILL
    df_indicators = pd.concat([price_sma_5_symbol, price_sma_10_symbol, price_sma_20_symbol,
                               price_sma_50_symbol, price_sma_200_symbol, bb10_pct_symbol,
                               bb20_pct_symbol, bb50_pct_symbol, rsi5_symbol,
                               rsi10_symbol, macd_symbol, mom_symbol, vama_symbol], axis=1)

    df_indicators.fillna(0, inplace=True)

    return df_indicators


def write_predictions_to_csv(start_date, end_date, percent_gain, path, debug=False):
    date_range = pd.date_range(start_date, end_date)
    buy_data = dict()
    sell_data = dict()
    for date in date_range:
        predictions_dictionary = get_list_of_predicted_stocks(percent_gain, date)
        buy_signal_recognized_list = predictions_dictionary['buy_signal_recognized_list']
        buy_signal_recognized_str = '_'.join(buy_signal_recognized_list)
        sell_signal_recognized_list = predictions_dictionary['sell_signal_recognized_list']
        sell_signal_recognized_str = '_'.join(sell_signal_recognized_list)
        buy_data[date] = buy_signal_recognized_str
        sell_data[date] = sell_signal_recognized_str

    df_buy = pd.DataFrame(buy_data.items(), columns=['Date', 'Symbols'])
    df_buy = df_buy.set_index('Date')
    df_buy.to_csv(os.path.join(path, f'buy_predictions.csv'))

    df_sell = pd.DataFrame(sell_data.items(), columns=['Date', 'Symbols'])
    df_sell = df_sell.set_index('Date')
    df_sell.to_csv(os.path.join(path, f'sell_predictions.csv'))


def read_predictions(given_date, minimum_count=0, buy=True, debug=False):
    df = pd.read_csv(f'trading_assistant_app/predictions/{"buy_predictions" if buy else "sell_predictions"}.csv')
    df = df.set_index('Date')
    try:
        symbols = df['Symbols'][given_date]
    except KeyError as e:
        print(f'Invalid given_date index/key for {e}')
        symbols = ''

    if isinstance(symbols, float):
        if np.isnan(symbols):
            return []
    elif isinstance(symbols, str):
        predictions_list = symbols.split('_')
        filtered = filter(lambda symbol:
                          get_wsb_volume_for_date(symbol, given_date)['wsb_volume'] > minimum_count, predictions_list)
        filtered_list = list(filtered)
        return filtered_list


if __name__ == '__main__':
    debug = False
    percent_gain = 0.03
    path = os.path.join('trading_assistant_app', 'predictions')
    requested_date = '2021-11-24'
    start_time = dt.datetime.now()
    # Import Data Logic
    # reddit_files = [f.split('_rss.csv')[0] for f in os.listdir('trading_assistant_app/reddit_data')]
    # import_function(reddit_files)  # Gathers data for S&P 500 Stocks
    # gather_download_data(start_date, end_date, True)  # Gathers data for Custom stocks in symbols_config.json

    # Data Preparation & Prediction Logic
    # predicted_stocks_dictionary = get_list_of_predicted_stocks(percent_gain, requested_date)
    # buy_signal_recognized_list = predicted_stocks_dictionary['buy_signal_recognized_list']
    # len_files = predicted_stocks_dictionary['len_files']
    # empty_df_count = predicted_stocks_dictionary['empty_df_count']

    # Write predictions to CSV & Read them
    start_date = dt.datetime(2021, 11, 1)
    end_date = dt.datetime(2021, 12, 1)
    # write_predictions_to_csv(start_date, end_date, percent_gain, path)
    # pred = read_predictions(requested_date)
    # filter_reddit_count('2021-11-15', 0, buy_predictions=True)
    end_time = dt.datetime.now()

    print(f'--------------------------------------------')
    print('STATS')
    print(f'Time taken: {end_time - start_time}')
    # print(f'Number of Stock Symbols Recognized: {len(buy_signal_recognized_list)}/{len_files - empty_df_count}')
    # print()
    # print('RESULTS')
    # print(f'For date {requested_date}, the following are good stocks with an estimated percent gain {percent_gain}%')
    # [print(stock) for stock in buy_signal_recognized_list]
    print(f'--------------------------------------------')
