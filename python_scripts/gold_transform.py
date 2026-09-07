import pandas as pd

def dim_customer(custdf):
    dim=custdf[["cust_id", "cust_unq_id", "cust_name","cust_city", "cust_state", "cust_zipcode"]].drop_duplicates(subset=['cust_id'])
    print(f"  dim_customers: {len(dim)} rows")
    
    return dim

def dim_product(productdf,productNameEngdf):
    dim=productdf.merge(
        productNameEngdf[["prod_cat_name", "prod_cat_name_eng"]],
        on='prod_cat_name',
        how='left'
    )
    dim = dim[[
        "prod_id", "prod_cat_name", "prod_cat_name_eng",
        "prod_weight_g", "prod_length_cm", "prod_height_cm", "prod_width_cm",
    ]].drop_duplicates(subset=["prod_id"])
    print(f"  dim_products: {len(dim)} rows")
    
    return dim
    
def dim_seller(sellerdf):
    dim = sellerdf[[
        "seller_id", "seller_city", "seller_state", "seller_zipcode",
    ]].drop_duplicates(subset=["seller_id"])
    print(f"  dim_sellers: {len(dim)} rows")
    
    return dim

def build_fact_order_items(order_details_df, orders_df, payment_df, customers_df):
    payment_agg=(
        payment_df.groupby('order_id')['payment_value']
        .sum()
        .reset_index()
        .rename(columns={"payment_value": "order_payment_value_total"})
    )
    
    orders_df=orders_df.copy()
    for col in ["purchase_timestamp", "approved_at", "delivered_carrier_date","delivered_customer_date", "estimated_delivery_date"]:
        orders_df[col]=pd.to_datetime(orders_df[col],errors='coerce')
        
    orders_df['order_year_month']=orders_df['purchase_timestamp'].dt.strftime('%Y-%m')
    
    orders_with_cust=orders_df.merge(
        customers_df[["cust_id", "cust_state"]],
        on='cust_id',
        how='left'
    )
    
    fact=order_details_df.merge(
        orders_with_cust[["order_id", "cust_id", "ord_status", "purchase_timestamp",
            "delivered_customer_date", "estimated_delivery_date",
            "order_year_month", "cust_state"]],
        on='order_id',
        how='left'
    ).merge(
        payment_agg,
        on='order_id',
        how='left'
    )
    
    fact["item_revenue"] = fact["price"] + fact["freight_val"]
    
    print(f"  fact_order_items: {len(fact)} rows")
    return fact

