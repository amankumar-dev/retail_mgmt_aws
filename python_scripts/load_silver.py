import boto3
from io import BytesIO
from python_scripts.extract import read_parquet_from_s3
from python_scripts.silver_transform import validate_silver,clear_dataframe
from python_scripts.metadata import ingestion
import uuid

DATASETS=[
    "customers",
    "geolocation",
    "orderDetails",
    "orders",
    "payment",
    "productNameEng",
    "products",
    "reviews",
    "sellers"    
]

s3=boto3.client('s3')
BUCKET_NAME="amandataeng-retail-de-2026"

def write_s3_silver(df,dataset):
    parquet_buffer=BytesIO()
    df.to_parquet(parquet_buffer,engine='pyarrow',index=False)
    
    silver_key=f'silver/{dataset}.parquet'
    
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=silver_key,
        Body=parquet_buffer.getvalue()
    )
    
    print(f"  -> written to s3://{BUCKET_NAME}/{silver_key}")
    
    
def silver_load():
    batch_id=str(uuid.uuid4())
    print(f"Starting Silver load. batch_id = {batch_id}\n")
    
    for dataset in DATASETS:
        bronze_key=f"bronze/{dataset}.parquet"
        
        df=read_parquet_from_s3(bronze_key)
        print(f"  read {dataset} -> {df.shape[0]} rows, {df.shape[1]} columns from Bronze")

        df=clear_dataframe(df,dataset)
        validate_silver(df,dataset)

        df=ingestion(df,dataset,batch_id)
        
        write_s3_silver(df,dataset)
        print()
    
    print(f"✅ Silver load complete for all {len(DATASETS)} datasets.")
        
silver_load()