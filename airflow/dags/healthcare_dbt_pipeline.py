from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Abhinav",
    "depends_on_past": False,
}

DBT_PROJECT_DIR = "/opt/airflow/dbt_project/healthcare_dbt"

with DAG(
    dag_id ="healthcare_dbt_pipeline",
    default_args =default_args,
    start_date= datetime(2026,1,1),
    schedule="@daily",
    catchup= False,
    tags=["healthcare", "dbt"],
) as dag:

    dbt_staging = BashOperator(
        task_id = "dbt_staging",
        cwd= DBT_PROJECT_DIR,
        bash_command= "dbt run --select staging",
    )

    dbt_dimensions = BashOperator(
        task_id = "dbt_dimensions",
        cwd= DBT_PROJECT_DIR,
        bash_command= "dbt run --select marts.dimensions",
    )

    dbt_facts = BashOperator(
        task_id = "dbt_facts",
        cwd= DBT_PROJECT_DIR,
        bash_command="dbt run --select marts.facts",
    )

    dbt_intermediate = BashOperator(
        task_id = "dbt_intermediate",
        cwd= DBT_PROJECT_DIR,
        bash_command= "dbt run --select intermediate",
    )

    dbt_tests = BashOperator(
        task_id = "dbt_tests",
        cwd= DBT_PROJECT_DIR,
        bash_command = "dbt test",
    )

    dbt_docs = BashOperator(
        task_id = "dbt_docs",
        cwd= DBT_PROJECT_DIR,
        bash_command= "dbt docs generate",
    )

    (
        dbt_staging
        >> dbt_dimensions
        >> dbt_facts
        >> dbt_intermediate
        >> dbt_tests
        >>dbt_docs
    )