from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="crypto_etl_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["crypto", "portfolio"],
) as dag:

    run_etl = BashOperator(
        task_id="run_crypto_etl",
        bash_command="python /opt/airflow/project/src/etl_crypto.py", # chemin vers docker
    )
