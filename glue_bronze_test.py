import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext

args=getResolvedOptions(sys.argv,['JOB_NAME'])

sc=SparkContext()
glueContext=GlueContext(sc)
spark=glueContext.spark_session

df=spark.read.parquet('s3://amandataeng-retail-de-2026/bronze/customers.parquet')

print(f"===== Row count: {df.count()} =====")
 
print("===== Schema =====")
df.printSchema()
 
print("===== First 5 rows =====")
df.show(5)