from datetime import datetime, timedelta
import sys
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from src.callbacks import pipeline_failure_callback

# --------------------------------------------------
# Project Path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.load_raw import load_all

# --------------------------------------------------
# Configuration
# --------------------------------------------------

DBT_PROJECT_DIR = "/opt/airflow/dbt_project/healthcare_dbt"
DBT_PROFILES_DIR = "/opt/airflow/dbt"

default_args = {
    "owner": "abhinav",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "email_on_failure": False,
    "email_on_retry": False,

    "on_failure_callback": pipeline_failure_callback,
}

doc_md = """
# Healthcare Data Warehouse Pipeline

Production ETL pipeline for the Healthcare Data Warehouse.

## Pipeline Flow

1. Load raw CSV files into PostgreSQL staging tables
2. Install dbt dependencies
3. Execute dbt transformations
4. Execute dbt data quality tests
5. Record pipeline execution metadata

## Technology

- Apache Airflow
- Python
- PostgreSQL
- dbt
- Docker

Author: Abhinav
"""

# --------------------------------------------------
# DAG
# --------------------------------------------------

with DAG(
    dag_id="healthcare_pipeline",
    description="Healthcare Data Warehouse ETL Pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["healthcare", "etl", "dbt"],
    doc_md=doc_md,
) as dag:

    # --------------------------------------------------
    # Load Raw Data
    # --------------------------------------------------

    extract_and_load_raw = PythonOperator(
        task_id="extract_and_load_raw",
        python_callable=load_all,
        op_kwargs={
            "airflow_run_id": "{{ run_id }}"
        },
    )

    # --------------------------------------------------
    # dbt Transformations
    # --------------------------------------------------

    transform_models = BashOperator(
        task_id="transform_models",
        bash_command=f"""
        set -e

        cd {DBT_PROJECT_DIR}

        dbt deps --profiles-dir {DBT_PROFILES_DIR}

        dbt run --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    # --------------------------------------------------
    # dbt Tests
    # --------------------------------------------------

    run_data_quality_tests = BashOperator(
        task_id="run_data_quality_tests",
        bash_command=f"""
        set -e

        cd {DBT_PROJECT_DIR}

        dbt test --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    # --------------------------------------------------
    # dbt Docs Generate
    # --------------------------------------------------

    generate_dbt_docs = BashOperator(
        task_id="generate_dbt_docs",
        bash_command=f"""
        
        cd {DBT_PROJECT_DIR} &&

        dbt docs generate --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    (
        extract_and_load_raw
        >> transform_models
        >> run_data_quality_tests
        >> generate_dbt_docs
    )