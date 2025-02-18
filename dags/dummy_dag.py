from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 18),
    'retries': 1,
}

# Instantiate the DAG
dag = DAG(
    'dummy_dag',
    default_args=default_args,
    description='A simple dummy DAG',
    schedule_interval='@daily',  # Runs daily
    catchup=False
)


# Define tasks
task_1 = DummyOperator(
    task_id='start',
    dag=dag
)

task_2 = DummyOperator(
    task_id='end',
    dag=dag
)

# Define dependencies
task_1 >> task_2
