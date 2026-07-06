CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.patients (

    patient_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(20),
    date_of_birth DATE,
    city VARCHAR(100),
    insurance_provider VARCHAR(100),
    registration_date DATE
);

CREATE TABLE IF NOT EXISTS staging.doctors (

    doctor_id VARCHAR(20) PRIMARY KEY,
    doctor_name VARCHAR(200),
    specialization VARCHAR(100),
    experience_years INT
);

CREATE TABLE IF NOT EXISTS staging.hospitals (

    hospital_id VARCHAR(20) PRIMARY KEY,
    hospital_name VARCHAR(200),
    location VARCHAR(100),
    hospital_type VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS staging.appointments (

    appointment_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20),
    doctor_id VARCHAR(20),
    hospital_id VARCHAR(20),
    appointment_date DATE,
    diagnosis_code VARCHAR(20),
    treatment_cost NUMERIC(12, 2),
    appointment_duration INT,
    status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS staging.treatments (

    treatment_id VARCHAR(20) PRIMARY KEY,
    appointment_id VARCHAR(20),
    treatment_name VARCHAR(200),
    treatment_category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS staging.billing (

    bill_id VARCHAR(20) PRIMARY KEY,
    appointment_id VARCHAR(20),
    billing_amount NUMERIC(12, 2),
    insurance_covered BOOLEAN,
    payment_status VARCHAR(50),
    payment_date DATE
)

