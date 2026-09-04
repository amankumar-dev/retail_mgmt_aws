import boto3
from io import BytesIO
import uuid
from python_scripts.extract import read_csv_from_s3
from python_scripts.metadata import ingestion

RAW_FILES = {
    "raw/customers.csv":       "customers",
    "raw/geolocation.csv":     "geolocation",
    "raw/orderDetails.csv":    "orderDetails",
    "raw/orders.csv":          "orders",
    "raw/payment.csv":         "payment",
    "raw/productNameEng.csv":  "productNameEng",
    "raw/products.csv":        "products",
    "raw/reviews.csv":         "reviews",
    "raw/sellers.csv":         "sellers",
}

BUCKET_NAME="amandataeng-retail-de-2026"
s3=boto3.client('s3')

def write_s3_bronze(df,dataset):
    parquet_buffer=BytesIO()
    df.to_parquet(parquet_buffer,engine='pyarrow',index=False)
    
    bronze_key=f'bronze/{dataset}.parquet'
    
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=bronze_key,
        Body=parquet_buffer.getvalue()
    )
    
    print(f"  -> written to s3://{BUCKET_NAME}/{bronze_key}")
    
def bronze_load():
    batch_id=str(uuid.uuid4())
    print(f"Starting Bronze load. batch_id = {batch_id}\n")
    
    for key,dataset in RAW_FILES.items():
        df=read_csv_from_s3(key)
        df=ingestion(df,dataset,batch_id=batch_id)
        write_s3_bronze(df,dataset)
        
    print(f"\n✅ Bronze load complete for all {len(RAW_FILES)} files. batch_id = {batch_id}")
    

    