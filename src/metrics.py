from pathlib import Path
from datetime import datetime


METRICS_FILE = Path("/opt/airflow/logs/pipeline_metrics.csv")


def write_metrics(rows_loaded):

    first_write = not METRICS_FILE.exists()

    with open(METRICS_FILE, "a") as f:

        if first_write:
            f.write("timestamp,rows_loaded\n")

        f.write(
            f"{datetime.now().isoformat()},{rows_loaded}\n"
        )