import boto3

s3=boto3.client('s3')

bucket_name='amandataeng-retail-de-2026'
prefix='raw/'

response=s3.list_objects_v2(
    Bucket=bucket_name,
    Prefix=prefix
)

for obj in response.get('Contents',[]):
    print(obj['Key'])
