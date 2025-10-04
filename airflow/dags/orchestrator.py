import sys
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta

sys.path.append('/opt/airflow/api-request')

def safe_main_callable():
    from insert_records import main
    return main()

default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date': datetime(2025, 10, 1),
    'catchup':False
}

dag = DAG(
    dag_id = 'weather-api-dbt-orchestrator',
    default_args = default_args,
    schedule=timedelta(minutes=60)
)

with dag: 
    task1 = PythonOperator(
        task_id = 'ingest_data_task',
        python_callable=safe_main_callable
    )

    task2 = DockerOperator(
        task_id = 'transform_data_task',
        image = 'ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command = 'run',
        working_dir = '/usr/app',
        mounts = [
            Mount(source = '/home/tminh/repos/weather_data_project/dbt/my_project',
                  target = '/usr/app',
                  type = 'bind'),
            Mount(source = '/home/tminh/repos/weather_data_project/dbt/profiles.yml',
                  target = '/root/.dbt/profiles.yml',
                  type='bind'),
        ],
        network_mode = 'weather_data_project_my-network',
        docker_url = 'unix://var/run/docker.sock',
        auto_remove='success'
    )

    task1 >> task2