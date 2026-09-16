import time
import boto3

BUCKET_NAME="amandataeng-retail-de-2026"
REGION="us-east-1"
ROLE_ARN="arn:aws:iam::308638207134:role/GlueRetailPipelineRole"
SCRIPT_LOCAL_PATH="glue_bronze_test.py"
SCRIPT_S3_KEY="scripts/glue_bronze_test.py"
JOB_NAME='retail_bronze_test_job'

s3=boto3.client('s3',region_name=REGION)
glue=boto3.client('glue',region_name=REGION)

def upload_script():
    s3.upload_file(
        SCRIPT_LOCAL_PATH,
        BUCKET_NAME,
        SCRIPT_S3_KEY
    )
    print(f"Uploaded script to s3://{BUCKET_NAME}/{SCRIPT_S3_KEY}")
    
def create_job():
    try:
        glue.create_job(
            Name=JOB_NAME,
            Role=ROLE_ARN,
            Command={
                "Name":'glueetl',
                "ScriptLocation":f"s3://{BUCKET_NAME}/{SCRIPT_S3_KEY}",
                "PythonVersion":"3"
            },
            DefaultArguments={
                "--job-language":'python',
                "--Tempdir":f"s3://{BUCKET_NAME}/glue-temp/"
            },
            GlueVersion='4.0',
            WorkerType='G.1X',
            NumberOfWorkers=2,
            Timeout=10
        )
        print(f"Created Glue job: {JOB_NAME}")
        
    except glue.exceptions.AlreadyExistsException:
        print(f"Job '{JOB_NAME}' already exists, skipping creation.")
        
def run_job():
    response=glue.start_job_run(JobName=JOB_NAME)
    run_id=response['JobRunId']
    print(f"Started job run: {run_id}")
    
    print("Waiting for job to finish (this takes a minute or two for Spark to start up)...")
    while True:
        status=glue.get_job_run(JobName=JOB_NAME,RunId=run_id)
        state=status['JobRun']['JobRunState']
        
        if state in ("SUCCEEDED", "FAILED", "STOPPED", "TIMEOUT"):
            break
        print(f"  ...state: {state}")
        time.sleep(10)
        
    print(f"\nFinal state: {state}")
    
    if state=='SUCCEEDED':
        execution_time=status['JobRun'].get('ExecutionTime','?')
        print(f"Execution time: {execution_time} seconds")
        print(f"\nTo see the actual print() output (row count, schema, sample rows),")
        print(f"go to AWS Console -> Glue -> Jobs -> {JOB_NAME} -> Runs tab -> click this run -> 'Output logs' link")
    else:
        error=status['JobRun'].get('ErrorMessage','no error message available')
        print(f'Error:{error}')
        print(f"Check AWS Console -> Glue -> Jobs -> {JOB_NAME} -> Runs tab for full logs")
        
    return run_id


upload_script()
create_job()
run_job()


