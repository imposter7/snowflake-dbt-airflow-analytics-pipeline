
from datetime import datetime
import subprocess

from airflow import DAG
from airflow.operators.python import PythonOperator


def run_command(command):
    result = subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=True,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)


def generate_data():
    run_command([
        "python",
        "/opt/airflow/scripts/generate_ecommerce_data.py",
    ])


def load_data():
    run_command([
        "python",
        "/opt/airflow/scripts/load_to_snowflake.py",
    ])


def run_dbt():
    run_command([
        "dbt", "run",
        "--project-dir", "/opt/airflow/dbt",
        "--profiles-dir", "/home/airflow/.dbt",
        "--exclude", "example",
        "--log-path", "/tmp/dbt_logs",
        "--target-path", "/tmp/dbt_target",
    ])


def test_dbt():
    run_command([
        "dbt", "test",
        "--project-dir", "/opt/airflow/dbt",
        "--profiles-dir", "/home/airflow/.dbt",
        "--exclude", "example",
        "--log-path", "/tmp/dbt_logs",
        "--target-path", "/tmp/dbt_target",
    ])


with DAG(
    dag_id="ecommerce_pipeline",
    description="Automated Snowflake and dbt e-commerce analytics pipeline",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["ecommerce", "snowflake", "dbt"],
) as dag:

    generate = PythonOperator(
        task_id="generate_ecommerce_data",
        python_callable=generate_data,
    )

    load = PythonOperator(
        task_id="load_to_snowflake",
        python_callable=load_data,
    )

    transform = PythonOperator(
        task_id="run_dbt_transformations",
        python_callable=run_dbt,
    )

    validate = PythonOperator(
        task_id="run_dbt_tests",
        python_callable=test_dbt,
    )

    generate >> load >> transform >> validate

