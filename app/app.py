import datetime as dt
import json
import os
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

from ImportSecurities import *
from utils.aws_util import *
from utils.data_util import *
from utils.indicators import *


def prepare_data(symbols, start_date, end_date, percent_gain, debug=False):
    dates = pd.date_range(start_date, end_date)
    df_array = list()
    # prices_df = get_closings(symbols, dates, base_dir='data')
    # prices_normed = normalize(prices_df)

    for symbol in symbols:
        stock_data = get_ohlcv(symbol, dates, base_dir='data')
        sma_symbol = sma(stock_data, window=5)
        ema_symbol = ema(stock_data, window=5)
        vama_symbol = vama(stock_data, window=5)
        y_columns = []

        # Compile TA into joined DF & FFILL / BFILL
        join_df = pd.concat([sma_symbol, ema_symbol, vama_symbol], axis=1)
        join_df.ffill(inplace=True)
        join_df.bfill(inplace=True)
        y_df = pd.DataFrame(index=stock_data.index)

        # Calculate % change for each column
        for column in join_df.columns:
            y_column_name = f'Y_{column}'
            join_df[column] = join_df[column].pct_change()
            # Check if percentage greater than specified % gain parameter
            y_df[y_column_name] = np.where(join_df[column] > percent_gain, 1, 0)
            y_columns.append(y_column_name)

        # Sum the values where column was > % gain parameter
        join_df['Y'] = y_df.sum(axis=1)
        # If sum > ~50%, Then Mark as a Buy Signal, Else Not a Buy Signal
        join_df['Y'] = np.where(join_df['Y'] > np.floor(len(y_columns) / 2), 1, 0)
        join_df = join_df.dropna()

        df_array.append(join_df)

        if debug:
            print(stock_data.head(n=20), '\n')
            print(sma_symbol.head(n=20), '\n')
            print(ema_symbol.head(n=20), '\n')
            print(vama_symbol.head(n=20), '\n')
            print(join_df.head(n=20), '\n')
            print(join_df.columns)
            print(join_df.head(n=20), '\n')
            print(y_df.head(n=20), '\n')

    return df_array


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

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
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
    empty_df_count = 0
    cwd = os.getcwd()
    data_directory = os.path.join(cwd, 'data')
    files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]
    symbols = [symbol.split('.csv')[0] for symbol in files]
    start_date = dt.datetime(2011, 11, 1)
    end_date = dt.date.today()
    df_array = prepare_data(symbols=symbols, start_date=start_date, end_date=end_date, percent_gain=percent_gain)
    for symbol, df in zip(symbols, df_array):
        if len(df) == 0:
            empty_df_count += 1
            continue
        df_prediction = train_model(df, symbol, debug=debug)
        try:
            if df_prediction[f'Y_{symbol}'][given_date] == 1:
                buy_signal_recognized_list.append(symbol)
        except KeyError as e:
            print(f'Invalid given_date index/key for {e}')

    return {
        'buy_signal_recognized_list': buy_signal_recognized_list,
        'len_files': len(files),
        'empty_df_count': empty_df_count
    }


if __name__ == '__main__':
    debug = False
    percent_gain = 0.003
    requested_date = '2021-11-24'
    start_time = dt.datetime.now()
    # import_function()  # Gathers data for S&P 500 Stocks
    # gather_download_data(start_date, end_date, True)  # Gathers data for Custom stocks in symbols_config.json
    predicted_stocks_dictionary = get_list_of_predicted_stocks(percent_gain, requested_date)
    buy_signal_recognized_list = predicted_stocks_dictionary['buy_signal_recognized_list']
    len_files = predicted_stocks_dictionary['len_files']
    empty_df_count = predicted_stocks_dictionary['empty_df_count']
    end_time = dt.datetime.now()

    print(f'--------------------------------------------')
    print('STATS')
    print(f'Time taken: {end_time - start_time}')
    print(f'Number of Stock Symbols Recognized: {len(buy_signal_recognized_list)}/{len_files - empty_df_count}')
    print()
    print('RESULTS')
    print(f'For date {requested_date}, the following are good stocks with an estimated percent gain {percent_gain}%')
    [print(stock) for stock in buy_signal_recognized_list]
    print(f'--------------------------------------------')
