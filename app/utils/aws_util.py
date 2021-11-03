import boto3


def get_s3_resource():
    return boto3.resource('s3')


def list_buckets(s3_resource):
    for bucket in s3_resource.buckets.all():
        print(bucket.name)


def list_bucket_objects(s3_resource, bucket_name):
    bucket = s3_resource.Bucket(bucket_name)
    for obj in bucket.objects.all():
        print(f'Key: {obj.key}, Last Modified: {obj.last_modified}')


def upload_file_to_bucket(s3_resource, bucket_name, file_name):
    data = open(file_name, 'rb')
    s3_resource.Bucket(bucket_name).put_object(Key=file_name, Body=data)
