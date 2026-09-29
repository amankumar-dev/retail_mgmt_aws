from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR='/home/ec2-user/retail_mgmt_aws'
PYTHON_BIN=f'{PROJECT_DIR}/retail_mgmt_venv/bin/python'

def run_module(module_name):
    return f'cd {PROJECT_DIR} && {PYTHON_BIN} -m python_scripts.{module_name}'

default_args={
    'owner':'aman',
    "retries":1
}

with DAG(
    dag_id='retail_pipeline',
    description='Bronze -> Silver -> Gold -> Athena Analytics -> Reports',
    default_args=default_args,
    start_date=datetime(2026,1,1),
    schedule_interval=None,
    catchup=False,
    tags=['retail','medallion']
) as dag:
    
    upload_dataset=BashOperator(
        task_id='upload_dataset',
        bash_command=run_module('upload_datasets')
    )
    
    bronze_load=BashOperator(
        task_id='bronze_load',
        bash_command=run_module('load_bronze')
    )
    
    silver_load=BashOperator(
        task_id='silver_load',
        bash_command=run_module('load_silver')
    )
    
    gold_load=BashOperator(
        task_id='gold_load',
        bash_command=run_module('load_gold')
    )
    
    athena_setup=BashOperator(
        task_id='athena_setup',
        bash_command=run_module('athena_setup')
    )
    
    reports=BashOperator(
        task_id='generate_reports',
        bash_command=run_module('generate_reports')
    )
    
    upload_dataset >> bronze_load >> silver_load >> gold_load >> athena_setup >> reports