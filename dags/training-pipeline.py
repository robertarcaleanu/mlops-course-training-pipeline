from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from steps.source import read_csv_from_s3
from steps.transform import transform_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),  # More robust start date
    'retries': 1,
}

with DAG(
    'ml_pipeline',
    default_args=default_args,
    schedule_interval='0 6 * * *',
    catchup=False,
) as dag:

    # Task to create the temp folder using BashOperator
    task_create_temp_folder = BashOperator(
        task_id='create_temp_folder',
        bash_command='mkdir -p /opt/airflow/temp',  # Make sure it's created in the airflow container's path
    )

    # Task to load data from S3
    task_load_data = PythonOperator(
        task_id='load_data_from_s3',
        python_callable=read_csv_from_s3,
        op_kwargs={"bucket_name": "dataset-mlops-robert", "file_key": "bank-full.csv"},
    )

    # Task to transform the data
    task_transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    # Task dependencies
    task_create_temp_folder >> task_load_data >> task_transform_data
