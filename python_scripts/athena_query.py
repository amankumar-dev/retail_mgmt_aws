import time
import boto3
from io import BytesIO
import pandas as pd

BUCKET_NAME="amandataeng-retail-de-2026"
DATABASE_NAME="retail_gold"
ATHENA_OUTPUT=f"s3://{BUCKET_NAME}/athena-query-results/"
REGION="us-east-1"

athena=boto3.client('athena',region_name=REGION)
s3=boto3.client('s3')

def run_ddl(query,database=DATABASE_NAME):
    response=athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database':database},
        ResultConfiguration={'OutputLocation':ATHENA_OUTPUT}
    )
    query_id=response['QueryExecutionId']
    
    while True:
        status=athena.get_query_execution(QueryExecutionId=query_id)
        state=status['QueryExecution']['Status']['State']
        
        if state in ('SUCCEEDED','FAILED','CANCELLED'):
            break
        time.sleep(1)
        
    if state != 'SUCCEEDED':
        reason=status['QueryExecution']['Status'].get('StateChangeReason','unknown error')
        raise RuntimeError(f"Query failed: {reason}\nQuery was:\n{query}")
    
    bytes_scanned = status["QueryExecution"]["Statistics"]["DataScannedInBytes"]
    mb_scanned = bytes_scanned / (1024 * 1024)
    estimated_cost = (bytes_scanned / (1024**4)) * 5  # $5 per TB
    print(f"  Data scanned: {mb_scanned:.3f} MB  (~${estimated_cost:.8f})")
    
    result_key = f"athena-query-results/{query_id}.csv"
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=result_key)
    df = pd.read_csv(BytesIO(obj["Body"].read()))
    return df


