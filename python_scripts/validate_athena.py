from python_scripts.athena_query import run_ddl

TABLES=["dim_customers", "dim_products", "dim_sellers", "fact_order_items"]

for table in TABLES:
    print(f"\nChecking {table}...")
    df=run_ddl(f'SELECT COUNT(*) AS row_count FROM {table}')
    print(df)
    
    