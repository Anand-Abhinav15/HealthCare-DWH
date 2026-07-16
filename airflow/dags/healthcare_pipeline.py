from datetime import datetime, timedelta
import sys
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

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

    # Retry failed tasks automatically
    "retries": 2,
    "retry_delay": timedelta(minutes=2),

    # Email (disabled for now)
    "email_on_failure": False,
    "email_on_retry": False,
}

doc_md = """
# Healthcare Data Warehouse Pipeline

This pipeline performs the complete ETL workflow for the Healthcare Data Warehouse.

## Steps

1. Load raw CSV data into PostgreSQL
2. Transform data using dbt
3. Execute dbt data quality tests

## Technology Stack

- Python
- PostgreSQL
- dbt
- Apache Airflow
- Docker

Author: Abhinav
"""

# --------------------------------------------------
# DAG Definition
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

    # -------------------------
    # Extract + Load Raw Tables
    # -------------------------

    extract_and_load_raw = PythonOperator(
        task_id="extract_and_load_raw",
        python_callable=load_all,
    )

    # -------------------------
    # dbt Transformations
    # -------------------------

    transform_models = BashOperator(
        task_id="transform_models",
        bash_command=f"""
        cd {DBT_PROJECT_DIR} &&
        dbt deps --profiles-dir {DBT_PROFILES_DIR} &&
        dbt run --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    # -------------------------
    # Data Quality Tests
    # -------------------------

    run_data_quality_tests = BashOperator(
        task_id="run_data_quality_tests",
        bash_command=f"""
        cd {DBT_PROJECT_DIR} &&
        dbt test --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    (
        extract_and_load_raw
        >> transform_models
        >> run_data_quality_tests
    )