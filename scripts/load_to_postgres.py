import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"

DATABASE_URL = (
    "postgresql+psycopg2://"
    "admin:admin123@localhost:5433/healthcare_dw"
)

engine = create_engine(DATABASE_URL)

def load_csv_to_postgres(csv_file, table_name):

    print(f"Loading {table_name}...")

    df = pd.read_csv(csv_file)

    df.to_sql(
        name=table_name,
        con=engine,
        schema="staging",
        if_exists="replace",
        index=False,
        method="multi"
    )

    print(f"{len(df)} rows inserted.")


if __name__ == "__main__":

    load_csv_to_postgres(RAW_DATA_DIR / "patients.csv", "patients")

    load_csv_to_postgres(RAW_DATA_DIR / "doctors.csv", "doctors")

    load_csv_to_postgres(RAW_DATA_DIR / "hospitals.csv", "hospitals")

    load_csv_to_postgres(RAW_DATA_DIR / "appointments.csv", "appointments")

    load_csv_to_postgres(RAW_DATA_DIR / "treatments.csv", "treatments")

    load_csv_to_postgres(RAW_DATA_DIR / "billing.csv", "billing")

    print("\nAll data loaded successfully.")
