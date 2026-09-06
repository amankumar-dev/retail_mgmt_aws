import pandas as pd

def clear_dataframe(df,dataset):
    original_row=len(df)
    
    # Standarize Column Name
    df.columns=[c.strip().lower().replace(" ","_") for c in df.columns]
    
    # Strip whitespace on string/object columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col]=df[col].apply(lambda x:x.strip() if isinstance(x,str) else x)
        
    # Drop exact duplicate-rows
    df=df.drop_duplicates()
    
    removed=original_row-len(df)
    
    print(f"  [{dataset}] cleaned: {original_row} -> {len(df)} rows ({removed} duplicates removed)")
    
    return df
    
def validate_silver(df,dataset):
    if len(df)==0:
        raise ValueError(f"Silver validation failed for '{dataset}': 0 rows after cleaning.")
    
    null_pur=(df.isnull().sum()/len(df)*100).round(1)
    high_null_val=null_pur[null_pur>50]
    
    if not high_null_val.empty:
        print(f"  [{dataset}] ⚠️  columns with >50% nulls:")
        print(f"    {high_null_val.to_dict()}")
        
    print(f"  [{dataset}] ✅ validation passed: {len(df)} rows")
    return True

    
