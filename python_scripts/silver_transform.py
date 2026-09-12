import pandas as pd

PRIMARY_KEYS = {
    "customers": ["cust_id"],
    "orders": ["order_id"],
    "orderDetails": ["order_id", "order_item_id"],
    "payment": ["order_id", "payment_seq"],
    "products": ["prod_id"],
    "sellers": ["seller_id"],
    "reviews": ["review_id"],
    "productNameEng": ["prod_cat_name"],
}


def clear_dataframe(df, dataset_name):
    original_rows = len(df)

    # Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Strip whitespace on string/object columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # Drop exact duplicate rows
    df = df.drop_duplicates()
    exact_dupes_removed = original_rows - len(df)

    # Drop duplicate primary keys (keep first occurrence)
    key_dupes_removed = 0
    key_cols = PRIMARY_KEYS.get(dataset_name)
    if key_cols:
        before_key_dedup = len(df)
        df = df.drop_duplicates(subset=key_cols, keep="first")
        key_dupes_removed = before_key_dedup - len(df)

    print(
        f"  [{dataset_name}] cleaned: {original_rows} -> {len(df)} rows "
        f"({exact_dupes_removed} exact duplicates, {key_dupes_removed} duplicate-key rows removed)"
    )

    return df


def validate_silver(df, dataset_name):
    """
    Basic Silver validation checkpoint.
    Raises an error if the dataset fails a sanity check, instead of
    silently writing bad data forward to Gold.
    """
    if len(df) == 0:
        raise ValueError(f"Silver validation failed for '{dataset_name}': 0 rows after cleaning.")

    # Report null percentage per column (informational, not a hard failure)
    null_pct = (df.isnull().sum() / len(df) * 100).round(1)
    high_null_cols = null_pct[null_pct > 50]
    if not high_null_cols.empty:
        print(f"  [{dataset_name}] ⚠️ columns with >50% nulls:")
        print(f"    {high_null_cols.to_dict()}")

    print(f"  [{dataset_name}] ✅ validation passed: {len(df)} rows")
    return True