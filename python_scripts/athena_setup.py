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
    
def create_tables():
    tables={
        "dim_customers":'''
            CREATE EXTERNAL TABLE IF NOT EXISTS dim_customers(
                cust_id STRING,
                cust_unq_id STRING,
                cust_name STRING,
                cust_city STRING,
                cust_state STRING,
                cust_zipcode DOUBLE   
            )
            STORED AS PARQUET
            LOCATION 's3://{bucket}/gold/dim_customers/'
        ''',
        
        "dim_products":'''
            CREATE EXTERNAL TABLE IF NOT EXISTS dim_products(
                prod_id STRING,
                prod_cat_name STRING,
                prod_cat_name_eng STRING,
                prod_weight_g DOUBLE,
                prod_length_cm DOUBLE,
                prod_height_cm DOUBLE,
                prod_width_cm DOUBLE
            )
            STORED AS PARQUET
            LOCATION 's3://{bucket}/gold/dim_products/'
        ''',
        
        "dim_sellers":'''
            CREATE EXTERNAL TABLE IF NOT EXISTS dim_sellers(
                seller_id STRING,
                seller_city STRING,
                seller_state STRING,
                seller_zipcode BIGINT
            )
            STORED AS PARQUET
            LOCATION 's3://{bucket}/gold/dim_sellers/'
        ''',
        
        "fact_order_items":'''
            CREATE EXTERNAL TABLE IF NOT EXISTS fact_order_items(
                order_id STRING,
                order_item_id BIGINT,
                prod_id STRING,
                seller_id STRING,
                shipp_limit_date STRING,
                price DOUBLE,
                freight_val DOUBLE,
                `timestamp` TIMESTAMP,
                source STRING,
                batch_id STRING,
                cust_id STRING,
                ord_status STRING,
                purchase_timestamp TIMESTAMP,
                delivered_customer_date TIMESTAMP,
                estimated_delivery_date TIMESTAMP,
                order_year_month STRING,
                cust_state STRING,
                order_payment_value_total DOUBLE,
                item_revenue DOUBLE
            )
            STORED AS PARQUET
            LOCATION 's3://{bucket}/gold/fact_order_items/'
        '''
    }
    
    for table_name,ddl_template in tables.items():
        print(f"Creating table '{table_name}'...")
        ddl=ddl_template.format(bucket=BUCKET_NAME)
        run_ddl(ddl,database=DATABASE_NAME)

        
create_database()
create_tables()
print(f"\n✅ Athena setup complete. Database: {DATABASE_NAME}")
print("Query results will land in:", ATHENA_OUTPUT)

