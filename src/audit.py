from datetime import datetime

from src.database import get_connection
from src.logger import logger


def log_pipeline_run(
    pipeline_name: str,
    run_start: datetime,
    run_end: datetime,
    status: str,
    rows_loaded: int,
    message: str = "",
    airflow_run_id: str | None = None,
    dbt_models: int = 0,
    tests_total: int = 0,
    tests_passed: int = 0,
    tests_failed: int = 0,
) -> None:
    """
    Store one pipeline execution in metadata.pipeline_audit.

    Parameters
    ----------
    pipeline_name : str
        Name of the pipeline.

    run_start : datetime
        Pipeline start time.

    run_end : datetime
        Pipeline end time.

    status : str
        SUCCESS / FAILED

    rows_loaded : int
        Total rows loaded into staging.

    message : str
        Error message if failed.

    airflow_run_id : str | None
        Airflow DAG Run ID.

    dbt_models : int
        Number of dbt models executed.

    tests_total : int
        Total dbt tests executed.

    tests_passed : int
        Number of passed dbt tests.

    tests_failed : int
        Number of failed dbt tests.
    """

    duration = round((run_end - run_start).total_seconds(), 2)

    insert_query = """
        INSERT INTO metadata.pipeline_audit
        (
            pipeline_name,
            airflow_run_id,
            run_start,
            run_end,
            duration_seconds,
            status,
            rows_loaded,
            dbt_models,
            tests_total,
            tests_passed,
            tests_failed,
            message
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        );
    """

    values = (
        pipeline_name,
        airflow_run_id,
        run_start,
        run_end,
        duration,
        status,
        rows_loaded,
        dbt_models,
        tests_total,
        tests_passed,
        tests_failed,
        message,
    )

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_query, values)
            conn.commit()

        logger.info(
            "Pipeline audit logged | "
            f"Status={status} | "
            f"Rows={rows_loaded} | "
            f"Duration={duration}s | "
            f"Models={dbt_models} | "
            f"Tests={tests_passed}/{tests_total}"
        )

    except Exception:
        logger.exception("Failed to write pipeline audit record.")
        raise