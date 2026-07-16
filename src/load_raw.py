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


def load_all():

    run_start = datetime.now()

    total_rows = 0

    status = "SUCCESS"

    message = ""

    try:

        logger.info("Starting raw data load...")

        for table in TABLES:

            df = load_csv(f"{table}.csv")

            truncate_table("staging", table)

            copy_dataframe(df, "staging", table)

            rows = len(df)

            total_rows += rows

            logger.info(f"{table} loaded ({rows} rows)")

        logger.info(f"Raw loading completed ({total_rows} rows).")

    except Exception as e:

        status = "FAILED"

        message = str(e)

        logger.exception("Pipeline failed.")

        raise

    finally:

        run_end = datetime.now()

        log_pipeline_run(
            pipeline_name="healthcare_pipeline",
            run_start=run_start,
            run_end=run_end,
            status=status,
            rows_loaded=total_rows,
            message=message,
        )