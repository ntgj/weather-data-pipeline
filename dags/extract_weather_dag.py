from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'coleta_clima_dag',
    default_args=default_args,
    description='Coleta de dados meteorológicos com WeatherAPI',
    schedule_interval=timedelta(minutes=15),
    start_date=datetime(2025, 5, 24),
    catchup=False,
) as dag:

    executar_coleta = BashOperator(
        task_id='executar_coleta',
        bash_command='python /opt/airflow/scripts/coleta_clima.py'
    )

    executar_coleta
