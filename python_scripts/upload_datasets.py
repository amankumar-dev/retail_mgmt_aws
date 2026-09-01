import boto3
from pathlib import Path

s3=boto3.client('s3')

s3_prefix='raw/'
bucket_name='amandataeng-retail-de-2026'
local_folder=Path('datasets')

for file in local_folder.iterdir():
    if file.is_file():
        s3_key=f'{s3_prefix}{file.name}'
        
        s3.upload_file(
            str(file),
            bucket_name,
            s3_key
        )
        
        print(f'Uploaded: {file.name}')
        
print('All file uploaded successfully')