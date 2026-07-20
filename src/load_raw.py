from datetime import datetime

from src.audit import log_pipeline_run
from src.extract import load_csv
from src.load import truncate_table, copy_dataframe
from src.logger import logger
from src.metrics import write_metrics
from src.validation import validate_row_counts


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

        logger.info("Starting raw data load...")

        validation_results = []

        for table in TABLES:

            df = load_csv(f"{table}.csv")

            truncate_table("staging", table)

            copy_dataframe(df, "staging", table)

            csv_rows = len(df)

            db_rows = validate_row_counts(table, csv_rows)

            validation_results.append(
                {
                    "table": table,
                    "csv_rows": csv_rows,
                    "db_rows": db_rows,
                }
            )

            total_rows += csv_rows

            logger.info(
                f"{table}: CSV={csv_rows} | Database={db_rows}"
            )

        write_metrics(total_rows)

        logger.info(
            f"Raw loading completed ({total_rows} rows)."
        )

    except Exception as e:

        status = "FAILED"

        message = str(e)

        logger.exception("Pipeline failed.")

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
            message=message,
        )