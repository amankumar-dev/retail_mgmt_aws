import pandas as pd

def ingestion(df,source,batch_id):
    df['timestamp']=pd.Timestamp.now()
    df['source']=source
    df['batch_id']=batch_id
    df.null=pd.notnull(None)