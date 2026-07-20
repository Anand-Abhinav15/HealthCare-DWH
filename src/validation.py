from src.database import get_connection


def validate_row_counts(table_name, csv_rows):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        f"""
        SELECT COUNT(*)
        FROM staging.{table_name}
        """
    )

    db_rows = cur.fetchone()[0]

    cur.close()

    conn.close()

    if csv_rows != db_rows:
        raise Exception(
            f"Row count mismatch for {table_name}. "
            f"CSV={csv_rows}, Database={db_rows}"
        )

    return db_rows