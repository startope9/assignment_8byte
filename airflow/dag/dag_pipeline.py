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
    dag_id='stock_market_pipeline',
    default_args=default_args,
    description='Fetch and store stock market data (Alpha Vantage -> Postgres)',
    schedule_interval='@daily', 
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    task_fetch_and_store = PythonOperator(
        task_id='fetch_and_store_stock_data',
        python_callable=fetch_and_store
    )

    task_fetch_and_store
