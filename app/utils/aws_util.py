import boto3
from botocore.exceptions import ClientError


def start_session(access_key_id, secret_access_key):
    return boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )


def get_s3_resource(session):
    return session.resource('s3')


def list_buckets(s3_resource):
    list_buckets = []
    for bucket in s3_resource.buckets.all():
        # print(bucket.name)
        list_buckets.append(bucket.name)
    return list_buckets


def list_objects(s3_resource, bucket_name):
    bucket = s3_resource.Bucket(bucket_name)
    list_objects = []
    for obj in bucket.objects.all():
        # print(f'Key: {obj.key}, Last Modified: {obj.last_modified}')
        list_objects.append(obj.key)
    return list_objects


def print_bucket_objects(s3_resource, bucket_name):
    objects = list_objects(s3_resource, bucket_name)
    bucket_str = f'Bucket: {bucket_name}'
    print(bucket_str)
    print(f'Number of objects: {len(objects)}')
    print("-" * len(bucket_str))
    for count, object in enumerate(objects):
        print(f'{count}) Object: {object}')
    print()


def delete_bucket(s3_resource, bucket_name):
    bucket = s3_resource.Bucket(bucket_name)
    response = bucket.delete()
    return response


def delete_object(s3_resource, bucket_name, object_name):
    response = s3_resource.Object(bucket_name, object_name).delete()
    return response


def upload_file_to_bucket(s3_resource, bucket_name, file_name, file_alias):
    data = open(file_name, 'rb')
    response = None
    try:
        response = s3_resource.Bucket(bucket_name).put_object(Key=file_alias, Body=data)
    except ClientError as e:
        print(e)
    return response
