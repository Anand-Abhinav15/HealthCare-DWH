from datetime import datetime

from src.audit import log_pipeline_run
from src.extract import load_csv
from src.load import truncate_table, copy_dataframe
from src.logger import logger


TABLES = [
    "patients",
    "appointments",
    "billing",
    "doctors",
    "hospitals",
    "treatments",
]


def load_all(airflow_run_id=None):

    run_start = datetime.now()

    total_rows = 0

    status = "SUCCESS"

    message = ""

    try:

        logger.info("=" * 60)
        logger.info("Starting raw data load...")
        logger.info(f"Airflow Run ID: {airflow_run_id}")
        logger.info("=" * 60)

        for table in TABLES:

            logger.info(f"Loading table: {table}")

            df = load_csv(f"{table}.csv")

            truncate_table("staging", table)

            copy_dataframe(df, "staging", table)

            rows = len(df)

            total_rows += rows

            logger.info(f"Loaded {rows:,} rows into staging.{table}")

        logger.info("=" * 60)
        logger.info(f"Raw loading completed successfully.")
        logger.info(f"Total rows loaded: {total_rows:,}")
        logger.info("=" * 60)

    except Exception as e:

        status = "FAILED"

        message = str(e)

        logger.exception("Pipeline execution failed.")

        raise

    finally:

        run_end = datetime.now()

        log_pipeline_run(
            pipeline_name="healthcare_pipeline",
            airflow_run_id=airflow_run_id,
            run_start=run_start,
            run_end=run_end,
            status=status,
            rows_loaded=total_rows,
            dbt_models=0,
            tests_total=0,
            tests_passed=0,
            tests_failed=0,
            message=message,
        )