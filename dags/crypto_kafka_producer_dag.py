from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="crypto_kafka_producer",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["crypto", "kafka", "portfolio"],
) as dag:

    run_producer = BashOperator(
        task_id="run_producer",
        bash_command="python /opt/airflow/project/src/producer_crypto.py --duration 60 --interval 30",
    )
