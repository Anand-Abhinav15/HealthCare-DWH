from datetime import datetime
import time

from src.audit import log_pipeline_run
from src.extract import load_csv
from src.load import truncate_table, copy_dataframe
from src.logger import logger
from src.metrics import write_metrics
from src.validation import validate_row_counts
from src.table_metrics import log_table_metrics


TABLES = [
    "patients",
    "appointments",
    "billing",
    "doctors",
    "hospitals",
    "treatments",
]


def load_all(**context):

    run_start = datetime.now()

    total_rows = 0

    status = "SUCCESS"

    message = ""

    airflow_run_id = None

    if context.get("dag_run"):
        airflow_run_id = context["dag_run"].run_id

    try:

        logger.info("=" * 70)
        logger.info("Starting Healthcare raw data load")
        logger.info(f"Airflow Run ID: {airflow_run_id}")
        logger.info("=" * 70)

        for table in TABLES:

            logger.info(f"Loading table: {table}")

            table_start = time.perf_counter()

            # Read CSV
            df = load_csv(f"{table}.csv")

            # Load to staging
            truncate_table("staging", table)

            copy_dataframe(df, "staging", table)

            csv_rows = len(df)

            # Validate load
            db_rows = validate_row_counts(table, csv_rows)

            table_duration = time.perf_counter() - table_start

            # Log table-level metrics
            log_table_metrics(
                pipeline_name="healthcare_pipeline",
                table_name=table,
                rows_loaded=db_rows,
                duration=table_duration,
            )

            total_rows += db_rows

            logger.info(
                f"{table}: CSV={csv_rows:,} | DB={db_rows:,} | "
                f"Duration={table_duration:.2f}s"
            )

        # Write lightweight CSV metrics
        write_metrics(total_rows)

        logger.info("=" * 70)
        logger.info(
            f"Raw loading completed successfully ({total_rows:,} rows)"
        )
        logger.info("=" * 70)

    except Exception as e:

        status = "FAILED"

        message = str(e)

        logger.exception("Pipeline execution failed")

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