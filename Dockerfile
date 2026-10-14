FROM apache/airflow:2.10.5

USER airflow

RUN pip install --no-cache-dir \
    "dbt-core==1.12.6" \
    "dbt-snowflake==1.12.3" \
    "pandas>=2.2,<3" \
    "faker>=30,<41"
