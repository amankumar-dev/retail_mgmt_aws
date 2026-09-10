from python_scripts.athena_query import run_ddl

def top_customer():
    query='''
        SELECT c.cust_id,COUNT(*) as repeat
        FROM customers c
    '''