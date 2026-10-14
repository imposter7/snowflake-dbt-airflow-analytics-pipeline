
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def check_pipeline():
    print("E-commerce pipeline initialized successfully!")
    print("Airflow is ready to orchestrate Snowflake and dbt.")


with DAG(
    dag_id="ecommerce_pipeline",
    description="E-commerce analytics pipeline using Snowflake and dbt",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["ecommerce", "snowflake", "dbt"],
) as dag:

    start_pipeline = PythonOperator(
        task_id="check_pipeline",
        python_callable=check_pipeline,
    )

