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
    
    df = pd.DataFrame(hospitals)

    df.to_csv(
        RAW_DATA_DIR / "hospitals.csv", index = False
    )

    return df


def generate_doctors():
    doctors = []

    for i in range(1, NUM_DOCTORS+1):
        doctors.append({
            "doctor_id": generate_id("D", i),
            "doctor_name": fake.name(),
            "specialization": random.choice(specializations),
            "experience_years": random.randint(1, 35)
        })

    df = pd.DataFrame(doctors)

    df.to_csv(RAW_DATA_DIR / "doctors.csv", index= False)

    return df


def generate_patients():
    patients = []

    for i in range(1, NUM_PATIENTS + 1):
        dob = fake.date_of_birth(minimum_age=1, maximum_age=90)

        patients.append({
            "patient_id": generate_id("P", i),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "gender": random.choice(["Male", "Female"]),
            "date_of_birth": dob,
            "city": random.choice(cities),
            "insurance_provider": random.choice(insurance_providers),
            "registration_date": fake.date_between(start_date = "-5y", end_date= "today")
        })
    
    df = pd.DataFrame(patients)

    df.to_csv(RAW_DATA_DIR / "patients.csv", index=False)

    return df


def generate_appointments(patients_df, doctors_df, hospitals_df):
    appointments = []

    patient_ids = patients_df["patient_id"].tolist()
    doctor_ids = doctors_df["doctor_id"].tolist()
    hospital_ids = hospitals_df["hospital_id"].tolist()

    for i in range(1, NUM_APPOINTMENTS + 1):

        treatment_cost = round(random.uniform(100, 5000), 2)

        appointments.append({
            "appointment_id": generate_id("A", i),
            "patient_id": random.choice(patient_ids),
            "doctor_id": random.choice(doctor_ids),
            "hospital_id": random.choice(hospital_ids),
            "appointment_date": fake.date_between(start_date="-3y", end_date="today"),
            "diagnosis_code": f"DX{random.randint(100, 999)}",
            "treatment_cost": treatment_cost,
            "appointment_duration": random.randint(15, 120),
            "status": random.choice(["Completed", "Cancelled", "Scheduled"]),
        })

    df = pd.DataFrame(appointments)

    df.to_csv(RAW_DATA_DIR / "appointments.csv", index=False)

    return df


def generate_treatments(appointments_df):
    treatments = []

    appointment_ids = appointments_df["appointment_id"].tolist()

    for i, appointment_id in enumerate(appointment_ids, start=1):
        treatments.append({
            "treatment_id": generate_id("T", i),
            "appointment_id": appointment_id,
            "treatment_name": random.choice([
                "MRI Scan", "X-Ray", "Consultation", "Physiotherapy", "Heart Surgery"
            ]),
            "treatment_category": random.choice(treatment_categories)
        })
            
    df = pd.DataFrame(treatments)

    df.to_csv(RAW_DATA_DIR / "treatments.csv", index=False)

    return df


def generate_billing(appointments_df):
    billing = []

    appointment_ids = appointments_df["appointment_id"].tolist()

    for i, row in enumerate(appointments_df.itertuples(), start=1):

        billing_amount= round(row.treatment_cost*random.uniform(1, 1.3), 2)

        billing.append({
            "billing_id": generate_id("B", i),
            "appointment_id": row.appointment_id,
            "billing_amount": billing_amount,
            "insurance_covered": random.choice([True, False]),
            "payment_status": random.choice(["Paid", "Pending", "Rejected"]),
            "payment_date": fake.date_between(start_date = "-3y", end_date = "today")
        })
    
    df = pd.DataFrame(billing)

    df.to_csv(RAW_DATA_DIR / "billing.csv", index=False)

    return df


if __name__ == "__main__":

    print("Generating hospitals...")
    hospitals = generate_hospitals()

    print("Generating doctors...")
    doctors = generate_doctors()

    print("Generating patients...")
    patients = generate_patients()

    print("Generating appointments...")
    appointments = generate_appointments(
        patients, doctors, hospitals
    )

    print("Generating treatments...")
    generate_treatments(appointments)

    print("Generating billing...")
    generate_billing(appointments)

    print("All datasets generated successfully!")

