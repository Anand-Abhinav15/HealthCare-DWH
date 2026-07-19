from datetime import datetime

from src.audit import update_pipeline_status
from src.logger import logger


def pipeline_failure_callback(context):
    """
    Executes whenever an Airflow task fails.
    Updates the pipeline audit table with FAILED status.
    """

    dag_run = context["dag_run"]

    task_instance = context["task_instance"]

    exception = context.get("exception")

    message = (
        f"Task '{task_instance.task_id}' failed. "
        f"Reason: {exception}"
    )

    logger.error(message)

    update_pipeline_status(
        airflow_run_id=dag_run.run_id,
        status="FAILED",
        message=message,
        run_end=datetime.now(),
    )