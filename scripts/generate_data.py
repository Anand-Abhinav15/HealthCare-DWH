import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path

fake = Faker()
random.seed(42)
Faker.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

NUM_PATIENTS = 10000
NUM_DOCTORS = 500
NUM_HOSPITALS = 50
NUM_APPOINTMENTS = 100000

insurance_providers = [
    "Aetna", "Cigna", "United Healthcare", "Blue Cross", "Humana"
]

specializations = [
    "cadiology", "neurology", "Orthopedics", "Dermatology", "Pediatrics",
    "Oncology", "General Medicine"
]

hospital_types = [
    "Government", "Private", "Teaching", "Specialty"
]

treatment_categories = [
    "Consultation", "Surgery", "Diagnostics", "Therapy"
]

cities =  [
    "New York", "Chicago", "Houston", "Boston", "Dallas", 
    "Seattle", "Miami", "San Francisco"
]


def generate_id(prefix, number):
    return f"{prefix}{number:06d}"


def generate_hospitals():
    hospitals = []

    for i in range(1, NUM_HOSPITALS +1):
        hospitals.append({
            "hospital_id": generate_id("H", i),
            "hospital_name": f"{fake.last_name()} Medical Center",
            "location": random.choice(cities),
            "hospital_type": random.choice(hospital_types)
            })
    
    df = pd.dataFrame(hospitals)

    df.to_csv(
        RAW_DATA_DIR / "hospitals.csv", index = False
    )

    return df


def generate_doctors():
    doctors = []

    for i in range(1, NUM_DOCTORS+1):
        pass






