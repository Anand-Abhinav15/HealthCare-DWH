from datetime import datetime

from src.database import execute_query


def log_pipeline_run(
    pipeline_name: str,
    run_start: datetime,
    run_end: datetime,
    status: str,
    rows_loaded: int,
    message: str = "",
):
    """
    Logs metadata about each pipeline execution.
    """

    duration = round((run_end - run_start).total_seconds(), 2)

    query = """
    INSERT INTO metadata.pipeline_audit
    (
        pipeline_name,
        run_start,
        run_end,
        status,
        rows_loaded,
        duration_seconds,
        message
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    execute_query(
        query,
        (
            pipeline_name,
            run_start,
            run_end,
            status,
            rows_loaded,
            duration,
            message,
        ),
    )