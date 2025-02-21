import logging

from airflow.providers.amazon.aws.hooks.s3 import S3Hook


def save_model_to_s3(s3_bucket='dataset-mlops-robert', s3_key='model_dag.joblib', aws_conn_id='aws-connection'):
    # Initialize the S3Hook to interact with S3
    logging.info("Start model saving")
    s3_hook = S3Hook(aws_conn_id=aws_conn_id)
    local_model_path = 'temp/model.joblib'
    
    # Upload the model to S3
    s3_hook.load_file(
        filename=local_model_path, 
        key=s3_key, 
        bucket_name=s3_bucket, 
        replace=True)
    
    logging.info("Model saved")
    
    