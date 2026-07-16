from src.extract import load_csv
from src.load import truncate_table, copy_dataframe
from src.logger import logger


TABLES = [
    "patients",
    "appointments",
    "billing",
    "doctors",
    "hospitals",
    "treatments",
]


def load_all():

    logger.info("Loading raw data...")

    for table in TABLES:

        df = load_csv(f"{table}.csv")

        truncate_table("staging", table)

        copy_dataframe(df, "staging", table)

        logger.info(f"{table} loaded ({len(df)} rows)")

    logger.info("Raw loading completed.")