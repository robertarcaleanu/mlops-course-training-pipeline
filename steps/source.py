from io import StringIO

import boto3
import pandas as pd


def read_csv_from_s3(bucket_name, file_key):
    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Get the object from the S3 bucket
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    
    # Read the CSV content
    csv_content = response['Body'].read().decode('utf-8')
    
    # Use StringIO to treat the string as file-like object and read it into pandas DataFrame
    csv_data = StringIO(csv_content)
    df = pd.read_csv(csv_data, sep=";")
    
    return df
