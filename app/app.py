import json
import os

from utils.aws_util import *
from utils.data_util import gather_data


def main():
    pass


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


def test_s3_upload():
    s3 = get_s3_resource()
    upload_file_to_bucket(s3, 'my-test-bucket', os.path.join(os.getcwd(), 'data', 'AAPL.csv'))
    list_bucket_objects(s3, 'my-test-bucket')


if __name__ == '__main__':
    # main()
    test_gather_data()
