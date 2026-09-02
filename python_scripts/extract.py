import boto3
import pandas as pd
from io import BytesIO

s3=boto3.client('s3')

bucket_name="amandataeng-retail-de-2026"

def read_csv_from_s3(s3_key):
    response=s3.get_object(
        Bucket=bucket_name,
        Key=s3_key
    )
    
    df=pd.read_csv(BytesIO(response['Body'].read()))
    
    return df

