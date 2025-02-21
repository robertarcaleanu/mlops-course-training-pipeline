from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from steps.source import read_csv_from_s3
from steps.train import train_model
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
    schedule_interval=None,
    catchup=False,
) as dag:

    # Task to create the temp folder using BashOperator
    task_create_temp_folder = BashOperator(
        task_id='create_temp_folder',
        bash_command='mkdir -p /opt/airflow/temp',  # Ensure temp folder is created
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

    task_train_model = PythonOperator(
        task_id='train_model',
        python_callable=train_model
    )

    # Task to remove the temp folder and its contents
    task_remove_temp_folder = BashOperator(
        task_id='remove_temp_folder',
        bash_command='rm -rf /opt/airflow/temp',  # Removes the temp folder and its contents
    )

    # Task dependencies
    task_create_temp_folder >> task_load_data >> task_transform_data >> task_train_model >> task_remove_temp_folder
