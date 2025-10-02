import sys
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

sys.path.append('/opt/airflow/api-request')

def safe_main_callable():
    from insert_records import main
    return main()

def example_task():
    print("This is an example task")

default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date': datetime(2025, 4, 30),
    'catchup':False
}

dag = DAG(
    dag_id = 'weather-api-orchestrator2',
    default_args = default_args,
    schedule=timedelta(minutes=60)
)

with dag: 
    task1 = PythonOperator(
        task_id = 'ingest_data_task',
        python_callable=safe_main_callable
    )
    #task 2
