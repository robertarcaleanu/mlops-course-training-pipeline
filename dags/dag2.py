from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

# Define default_args to be used in the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 15),
    'retries': 1,
}

# Initialize the DAG
dag = DAG(
    'dummy_dag2',  # DAG name
    default_args=default_args,
    description='A simple dummy DAG',
    schedule_interval=None,  # Set to None for manual execution or define a schedule interval
)

# Define a dummy task
dummy_task = DummyOperator(
    task_id='dummy_task',  # Task name
    dag=dag,
)

# Set the task sequence (though it's only one task here)
dummy_task
