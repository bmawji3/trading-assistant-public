import json
import os

from utils.aws_util import *
from utils.data_util import gather_data


def main():
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
    main()
