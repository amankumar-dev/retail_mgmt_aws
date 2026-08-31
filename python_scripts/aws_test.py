import boto3

s3=boto3.client('s3')

bucket_name='amandataeng-retail-de-2026'

s3.create_bucket(
    Bucket=bucket_name
)

print(f'Bucket created {bucket_name}')