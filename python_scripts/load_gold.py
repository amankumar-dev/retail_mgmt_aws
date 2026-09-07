from io import BytesIO
import boto3
from python_scripts.extract import read_parquet_from_s3
from python_scripts.gold_transform import dim_customer,dim_product,dim_seller,build_fact_order_items

BUCKET_NAME="amandataeng-retail-de-2026"
s3=boto3.client('s3')

def write_s3_gold(df,dataset):
    parquet_buffer=BytesIO()
    df=df.to_parquet(parquet_buffer,engine='pyarrow',index=False)
    
    gold_key=f'gold/{dataset}'
    
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=gold_key,
        Body=parquet_buffer.getvalue()
    )
    
    print(f"  -> written to s3://{BUCKET_NAME}/{gold_key}")
    
def gold_load():
    print("Starting Gold load...\n")
    print("Reading Silver tables...")
    
    customers = read_parquet_from_s3("silver/customers.parquet")
    products = read_parquet_from_s3("silver/products.parquet")
    product_name_eng = read_parquet_from_s3("silver/productNameEng.parquet")
    sellers = read_parquet_from_s3("silver/sellers.parquet")
    orders = read_parquet_from_s3("silver/orders.parquet")
    order_details = read_parquet_from_s3("silver/orderDetails.parquet")
    payment = read_parquet_from_s3("silver/payment.parquet")
    print("Done.\n")
    
    print("Building dimension tables...")
    dim_cust=dim_customer(customers)
    dim_sell=dim_seller(sellers)
    dim_prod=dim_product(products,product_name_eng)
    
    print("\nBuilding fact table...")
    fact_table=build_fact_order_items(order_details,orders,payment,customers)
    
    print("\nWriting to Gold...")
    write_s3_gold(dim_cust,'dim_customers')
    write_s3_gold(dim_sell,'dim_sellers')
    write_s3_gold(dim_prod,'dim_products')
    write_s3_gold(fact_table,'fact_table')
    
    print("\n✅ Gold load complete: dim_customers, dim_products, dim_sellers, fact_order_items")
    
gold_load()
    