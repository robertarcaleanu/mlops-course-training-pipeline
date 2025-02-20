import logging
from io import StringIO

import pandas as pd
from airflow.providers.amazon.aws.hooks.s3 import S3Hook  # Airflow 2.x hook import


def read_csv_from_s3(bucket_name, file_key):
    logging.info('Starting to read the data from S3')
    
    # Initialize S3Hook
    hook = S3Hook(aws_conn_id='aws-connection')  # Uses the 'aws_default' connection

    # Get the object from the S3 bucket
    response = hook.get_key(file_key, bucket_name)
    
    # Read the CSV content
    csv_content = response.get()['Body'].read().decode('utf-8')
    
    # Use StringIO to treat the string as file-like object and read it into pandas DataFrame
    csv_data = StringIO(csv_content)
    df = pd.read_csv(csv_data, sep=";")
    df = pd.concat([
        df[df['y'] == 'yes'],
        df[df['y'] == 'no'].head(len(df[df['y'] == 'yes']))
    ])

    logging.info('Starting to write data locally')
    df.to_parquet("temp/dataset.parquet")
    logging.info('Data stored locally')
