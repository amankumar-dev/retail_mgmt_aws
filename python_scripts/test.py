from python_scripts.extract import read_csv_from_s3

customers=read_csv_from_s3('raw/customers.csv')

print(customers)