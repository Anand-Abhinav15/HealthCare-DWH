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
    Logs pipeline execution metadata into metadata.pipeline_audit.
    """

    duration = round((run_end - run_start).total_seconds(), 2)

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
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
                    )
                    """,
                    (
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
                    ),
                )

            conn.commit()

        logger.info(
            f"Pipeline audit logged successfully "
            f"(status={status}, rows={rows_loaded}, duration={duration}s)"
        )

    except Exception:
        logger.exception("Failed to write pipeline audit log.")
        raise