"""
Diagnostic: checks each Silver table for duplicate keys.
Run: python -m python_scripts.diagnose_silver_keys
"""

from python_scripts.extract import read_parquet_from_s3

print("Checking orders...")
orders = read_parquet_from_s3("silver/orders.parquet")
print(f"  total rows: {len(orders)}")
print(f"  unique order_id: {orders['order_id'].nunique()}")
print(f"  unique cust_id: {orders['cust_id'].nunique()}")

print("\nChecking customers...")
customers = read_parquet_from_s3("silver/customers.parquet")
print(f"  total rows: {len(customers)}")
print(f"  unique cust_id: {customers['cust_id'].nunique()}")

print("\nChecking orderDetails...")
order_details = read_parquet_from_s3("silver/orderDetails.parquet")
print(f"  total rows: {len(order_details)}")
print(f"  unique order_id: {order_details['order_id'].nunique()}")

print("\nChecking payment...")
payment = read_parquet_from_s3("silver/payment.parquet")
print(f"  total rows: {len(payment)}")
print(f"  unique order_id: {payment['order_id'].nunique()}")

print("\n--- Simulating the Gold merges to find where it blows up ---")

orders_with_cust = orders.merge(
    customers[["cust_id", "cust_state"]], on="cust_id", how="left"
)
print(f"orders x customers -> {len(orders_with_cust)} rows (should stay ~{len(orders)})")

payment_agg = payment.groupby("order_id")["payment_value"].sum().reset_index()
print(f"payment_agg unique order_id rows: {len(payment_agg)}")

step1 = order_details.merge(
    orders_with_cust[["order_id", "cust_id", "cust_state"]], on="order_id", how="left"
)
print(f"order_details x orders_with_cust -> {len(step1)} rows (should stay ~{len(order_details)})")

step2 = step1.merge(payment_agg, on="order_id", how="left")
print(f"step1 x payment_agg -> {len(step2)} rows (should stay ~{len(order_details)})")