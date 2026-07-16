from database import get_connection


def execute_sql(path):

    conn = get_connection()
    cur = conn.cursor()

    with open(path, "r") as f:
        cur.execute(f.read())

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":

    execute_sql("src/sql/create_schemas.sql")
    execute_sql("src/sql/create_tables.sql")

    print("Database initialized successfully.")