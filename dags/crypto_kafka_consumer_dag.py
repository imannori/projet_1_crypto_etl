from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="crypto_kafka_consumer",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["crypto", "kafka", "portfolio"],
) as dag:

    run_consumer = BashOperator(
        task_id="run_consumer",
        bash_command="python /opt/airflow/project/src/consumer_crypto.py --duration 30",
    )