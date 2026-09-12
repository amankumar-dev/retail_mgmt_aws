from python_scripts.athena_query import run_ddl
import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

def top_customer():
    print("\n===== Top 10 Customers by Revenue =====")
    query='''
        SELECT 
            f.cust_id,
            c.cust_name,
            SUM(f.item_revenue) as total_revenue
        FROM fact_order_items f
        JOIN dim_customers c
        ON f.cust_id=c.cust_id
        GROUP BY f.cust_id,c.cust_name
        ORDER BY total_revenue desc
        LIMIT 10
    '''
    return run_ddl(query)

def repeat_customer():
    print("\n===== Repeat Customers (more than 1 order) =====")
    query='''
        SELECT f.cust_id,c.cust_name,COUNT(DISTINCT f.order_id) as repeat
        FROM fact_order_items f
        JOIN dim_customers c
        ON f.cust_id=c.cust_id
        GROUP BY f.cust_id,c.cust_name
        HAVING COUNT(DISTINCT f.order_id)>1
        ORDER BY repeat DESC
        LIMIT 10
    '''
    return run_ddl(query)

def revenue_per_customer():
    print("\n===== Revenue Per Customer (top 10 by avg order value) =====")
    query='''
        SELECT 
            f.cust_id,
            c.cust_name,
            SUM(f.item_revenue) as total_rev,
            COUNT(DISTINCT f.order_id) as orders,
            SUM(f.item_revenue)/COUNT(DISTINCT f.order_id) as avg_order_val
        FROM fact_order_items f
        JOIN dim_customers c
        ON f.cust_id=c.cust_id
        GROUP BY f.cust_id,c.cust_name
        ORDER BY avg_order_val DESC
        LIMIT 10
    '''
    return run_ddl(query)

def monthly_revenue():
    print("\n===== Monthly Revenue =====")
    query = """
        SELECT order_year_month, SUM(item_revenue) AS monthly_revenue
        FROM fact_order_items
        WHERE order_year_month IS NOT NULL
        GROUP BY order_year_month
        ORDER BY order_year_month
    """
    return run_ddl(query)
 
def revenue_by_state():
    print("\n===== Revenue by State =====")
    query='''
        SELECT f.cust_state,SUM(f.item_revenue) as total_rev
        FROM fact_order_items f
        WHERE f.cust_state IS NOT NULL
        GROUP BY f.cust_state
        ORDER BY total_rev DESC
    '''
    return run_ddl(query)

def product_contribution():
    print("\n===== Product Category Contribution =====")
    query='''
        SELECT 
            p.prod_cat_name_eng,
            SUM(f.item_revenue) as contribution
            FROM dim_products p
            JOIN fact_order_items f
            ON p.prod_id=f.prod_id
            WHERE p.prod_cat_name_eng IS NOT NULL
            GROUP BY p.prod_cat_name_eng
            ORDER BY contribution DESC
            LIMIT 10
    '''
    return run_ddl(query)

print(top_customer())
print(repeat_customer())
print(revenue_per_customer())
print(monthly_revenue())
print(revenue_by_state())
print(product_contribution())

