import boto3
import time

BUCKET_NAME="amandataeng-retail-de-2026"
DATABASE_NAME="retail_gold"
ATHENA_OUTPUT=f"s3://{BUCKET_NAME}/athena-query-results/"
REGION="us-east-1"

athena=boto3.client('athena',region_name=REGION)

def run_ddl(query,database=None):
    kwargs={
        "QueryString":query,
        "ResultConfiguration":{"OutputLocation":ATHENA_OUTPUT}
    }
    
    if database:
        kwargs["QueryExecutionContext"]={"Database":database}
        
    response=athena.start_query_execution(**kwargs)
    query_id=response["QueryExecutionId"]
    
    while True:
        status=athena.get_query_execution(QueryExecutionId=query_id)
        state=status["QueryExecution"]["Status"]["State"]
        
        if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
            break;
        time.sleep(1)
        
    if state!="SUCCEEDED":
        reason=status["QueryExecution"]["Status"].get("StateChangeReason","unknown error")
        raise RuntimeError(f"Query failed: {reason}\nQuery was:\n{query}")
    
    print(f"  ✅ succeeded (query_id={query_id})")
    return query_id

def create_database():
    print(f"Creating database '{DATABASE_NAME}' (if not exists)...")
    run_ddl(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    
