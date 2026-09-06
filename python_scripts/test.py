"""
Quick inspection script - run this and share the output.
Prints column names + dtypes + first 3 rows for each Silver table,
so we can correctly design the Gold layer joins (which columns are
keys, which are dates, which are amounts, etc).
"""

from python_scripts.extract import read_parquet_from_s3

DATASETS = [
    "customers",
    "geolocation",
    "orderDetails",
    "orders",
    "payment",
    "productNameEng",
    "products",
    "reviews",
    "sellers",
]

for dataset_name in DATASETS:
    print(f"\n===== {dataset_name} =====")
    df = read_parquet_from_s3(f"silver/{dataset_name}.parquet")
    print("Columns + dtypes:")
    print(df.dtypes)
    print("\nSample rows:")
    print(df.head(3).to_string())