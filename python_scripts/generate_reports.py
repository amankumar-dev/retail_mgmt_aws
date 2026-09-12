import matplotlib
import matplotlib.pyplot as plt
import boto3
import os
from io import BytesIO
from python_scripts.business_analytics import (
    top_customer,
    monthly_revenue,
    revenue_by_state,
    product_contribution,
)


BUCKET_NAME="amandataeng-retail-de-2026"
s3=boto3.client('s3')
LOCAL_FOLDER_NAME='reports'

os.makedirs(LOCAL_FOLDER_NAME,exist_ok=True)
matplotlib.use("Agg") 

def save_chart(fig,filename):
    local_path=os.join.path(LOCAL_FOLDER_NAME,filename)
    fig.savefig(local_path,bbox_inches='tight',dpi=100)
    print(f"  saved locally: {local_path}")
    
    buffer=BytesIO()
    
    fig.savefig(buffer,format='png',bbox_inches='tight',dpi=100)
    
    buffer.seek(0)
    
    key=f'reporst/{filename}'
    s3.put_objects(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=buffer.getvalue()
    )
    print(f"  uploaded to: s3://{BUCKET_NAME}/{key}")
    
    plt.close(fig)
    
def chart_top_customers():
    print("\nGenerating Top Customers chart...")
    
    df=top_customer()
    fig,ax=plt.subplot(figsize=(10,6))
    ax.barh(df['cust_name'],df['total_revenue'],color='#2E86AB')
    ax.set_xlabel(df['total_revenue'])
    ax.set_ylabel(df['cust_name'])
    

    