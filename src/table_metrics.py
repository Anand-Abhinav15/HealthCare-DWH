from src.database import get_connection


def log_table_metrics(
    pipeline_name,
    table_name,
    rows_loaded,
    duration,
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO metadata.table_load_metrics
        (
            pipeline_name,
            table_name,
            rows_loaded,
            load_duration_seconds
        )
        VALUES (%s,%s,%s,%s)
        """,
        (
            pipeline_name,
            table_name,
            rows_loaded,
            round(duration, 2),
        ),
    )

    conn.commit()

    cur.close()

    conn.close()