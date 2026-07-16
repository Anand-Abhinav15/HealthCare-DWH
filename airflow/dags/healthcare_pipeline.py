from datetime import datetime
import sys
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Allow Airflow to import the src package
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.load_raw import load_all


default_args = {
    "owner": "abhinav",
}


with DAG(
    dag_id="healthcare_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["healthcare", "etl"],
) as dag:

    load_raw = PythonOperator(
        task_id="load_raw_data",
        python_callable=load_all,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        cd /opt/airflow/dbt_project/healthcare_dbt &&
        dbt deps --profiles-dir /opt/airflow/dbt &&
        dbt run --profiles-dir /opt/airflow/dbt
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
        cd /opt/airflow/dbt_project/healthcare_dbt &&
        dbt test --profiles-dir /opt/airflow/dbt
        """,
    )

    load_raw >> dbt_run >> dbt_test