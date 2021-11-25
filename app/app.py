import datetime as dt
import json
import os
import pandas as pd

from utils.aws_util import *
from utils.data_util import *
from utils.indicators import *


def test_prepare_data(symbols, start_date, end_date, percent_gain, debug=False):
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
        # If sum > 50%, Then Mark as a Buy Signal, Else Not a Buy Signal
        join_df['Y'] = np.where(join_df['Y'] > np.ceil(len(y_columns) / 2), 1, 0)
        join_df.name = symbol

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


def test_s3_functions():
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


def test_gather_data():
    download_new_data = False
    symbols_config_fp = os.path.join(os.getcwd(), 'config', 'symbols_config.json')
    with open(symbols_config_fp) as fp:
        symbols_config = json.load(fp)

    print(symbols_config)
    symbols_array = []
    for category, array in symbols_config.items():
        symbols_array.append(array)
    flat_symbols = [item for sublist in symbols_array for item in sublist]

    if download_new_data:
        spaces_array = []
        for array in symbols_array:
            spaces = " ".join(array)
            spaces_array.append(spaces)
        gather_data(symbols_array, spaces_array)


if __name__ == '__main__':
    symbols = ['FB', 'AAPL']
    start_date = dt.datetime(2021, 1, 15)
    end_date = dt.datetime(2021, 4, 27)
    df_array = test_prepare_data(symbols=symbols, start_date=start_date, end_date=end_date, percent_gain=0.001)
    for df in df_array:
        print('-' * len(str(df.name)))
        print(df.name)
        print('-' * len(str(df.name)))
        print()
        print(df)
        print()
