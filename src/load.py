from io import StringIO

from src.database import get_connection


def truncate_table(schema, table):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(f"TRUNCATE TABLE {schema}.{table} RESTART IDENTITY CASCADE")

    conn.commit()

    cur.close()

    conn.close()


def copy_dataframe(df, schema, table):

    conn = get_connection()

    cur = conn.cursor()

    buffer = StringIO()

    df.to_csv(buffer, index=False, header=False)

    buffer.seek(0)

    cur.copy_expert(
        f"""
        COPY {schema}.{table}
        FROM STDIN
        WITH CSV
        """,
        buffer,
    )

    conn.commit()

    cur.close()

    conn.close()