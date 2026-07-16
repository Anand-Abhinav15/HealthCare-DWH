import os

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Creates and returns a PostgreSQL connection.
    """

    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def execute_query(query, params=None):
    """
    Executes INSERT, UPDATE, DELETE or DDL statements.
    """

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)

        conn.commit()

    finally:
        conn.close()


def fetch_query(query, params=None):
    """
    Executes a SELECT query and returns all rows.
    """

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    finally:
        conn.close()


def bulk_insert(table_name, columns, rows):
    """
    Efficient bulk insert using psycopg2.execute_values().
    """

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            query = f"""
                INSERT INTO {table_name}
                ({",".join(columns)})
                VALUES %s
            """

            execute_values(cursor, query, rows)

        conn.commit()

    finally:
        conn.close()