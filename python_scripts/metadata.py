import pandas as pd

def ingestion(df,source,batch_id):
    df=df.where(pd.notnull(df),None)
    df=df.astype(object)
    df['timestamp']=pd.Timestamp.now()
    df['source']=source
    df['batch_id']=batch_id
    
    return df