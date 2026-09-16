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
    local_path=os.path.join(LOCAL_FOLDER_NAME,filename)
    fig.savefig(local_path,bbox_inches='tight',dpi=100)
    print(f"  saved locally: {local_path}")
    
    buffer=BytesIO()
    
    fig.savefig(buffer,format='png',bbox_inches='tight',dpi=100)
    
    buffer.seek(0)
    
    key=f'reports/{filename}'
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=buffer.getvalue()
    )
    print(f"  uploaded to: s3://{BUCKET_NAME}/{key}")
    
    plt.close(fig)
    
def chart_top_customers():
    print("\nGenerating Top Customers chart...")
    
    df=top_customer()
    fig,ax=plt.subplots(figsize=(10,6))
    ax.barh(df['cust_name'],df['total_revenue'],color='#2E86AB')
    ax.set_xlabel('Total Revenue')
    ax.set_title('Top 10 customers')
    ax.invert_yaxis()
    save_chart(fig,"top_customers.png")
    
def chart_monthly_revenue():
    print("\nGenerating Monthly Revenue chart...")
    
    df=monthly_revenue()
    fig,ax=plt.subplots(figsize=(10,6))
    ax.plot(df['order_year_month'],df['monthly_revenue'],marker='o',color="#A23B72")
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue')
    ax.set_title('Monthly Revenue')
    plt.xticks(rotation=45,ha='right')
    save_chart(fig,'monthly_revenue.png')
    
def chart_revenue_by_state():
    print("\nGenerating Revenue by State chart...")
    
    df=revenue_by_state()
    fig,ax=plt.subplots(figsize=(10,6))
    ax.barh(df['cust_state'],df['total_rev'],color='#F18F01')
    ax.set_xlabel('Revenue')
    ax.set_ylabel('State')
    ax.set_title('Revenue by State')
    ax.invert_yaxis()
    save_chart(fig,'state_revenue.png')
    
def chart_product_contribution():
    print('\nGenerating Product Contribution chart...')
    
    df=product_contribution()
    fig,ax=plt.subplots(figsize=(10,6))
    ax.bar(df['prod_cat_name_eng'],df['contribution'],color='#3B8686')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Contribution')
    ax.set_title('Product Contribution')
    plt.xticks(rotation=45, ha="right")
    save_chart(fig,'prodcut_contribution.png')
    
chart_top_customers()
chart_monthly_revenue()
chart_revenue_by_state()
chart_product_contribution()
    
