from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from fetch import fetch_and_store

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='pipeline',
    default_args=default_args,
    description='fetch market data',
    schedule_interval='@daily', 
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    fetch = PythonOperator(
        task_id='fetch',
        python_callable=fetch_and_store
    )

    fetch
