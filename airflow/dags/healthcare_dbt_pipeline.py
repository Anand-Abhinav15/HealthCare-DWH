from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Abhinav",
    "depends_on_past": False,
}

with DAG(
    dag_id ="healthcare_dbt_pipeline",
    default_args =default_args,
    start_date= datetime(2026,1,1),
    schedule="@daily",
    catchup= False,
    tags=["healthcare", "dbt"],
) as dag:

    dbt_run = BashOperator(
        task_id = "dbt_run",
        cwd= "/opt/airflow/dbt_project/healthcare_dbt",
        bash_command= """
        dbt deps
        dbt run
        """
    )

    dbt_test = BashOperator(
        task_id = "dbt_test",
        cwd = "/opt/airflow/dbt_project/healthcare_dbt",
        bash_command= """
        dbt test
        """
    )

    dbt_docs = BashOperator(
        task_id="dbt_docs",
        cwd="/opt/airflow/dbt_project/healthcare_dbt",
        bash_command="""
        dbt docs generate
        """
    )

    dbt_run >> dbt_test >> dbt_docs