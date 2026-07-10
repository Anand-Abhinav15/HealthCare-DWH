--CTE1- Appointments

WITH appointments AS (
    SELECT *
    FROM {{ ref('stg_appointments') }}
),

--CTE2- Billing

billing AS (
    SELECT *
    FROM {{ ref('stg_billing') }}
),

--CTE3- Patient Dimension

patients AS (
    SELECT
        patient_key,
        patient_id
    FROM {{ ref('dim_patient') }}
),

--CTE4- Doctor Dimension

doctors AS (
    SELECT
        doctor_key,
        doctor_id
    FROM {{ ref('dim_doctor') }}
),

--CTE5- Hospital Dimension

hospitals AS (
    SELECT
        hospital_key,
        hospital_id
    FROM {{ ref('dim_hospital') }}
),

--CTE6- Date Dimension

dates AS (
    SELECT
        date_key,
        full_date
    FROM {{ ref('dim_date') }}
)


--Warehouse_Join

SELECT
    {{ dbt_utils.generate_surrogate_key(['appointments.appointment_id']) }}
        AS appointment_key,
    appointments.appointment_id,
    patients.patient_key,
    doctors.doctor_key,
    hospitals.hospital_key,
    dates.date_key,
    appointments.treatment_cost,
    billing.billing_amount,
    appointments.appointment_duration,
    appointments.status
FROM appointments

LEFT JOIN billing
    ON appointments.appointment_id = billing.appointment_id
LEFT JOIN patients
    ON appointments.patient_id = patients.patient_id
LEFT JOIN doctors
    ON appointments.doctor_id = doctors.doctor_id
LEFT JOIN hospitals
    ON appointments.hospital_id = hospitals.hospital_id
LEFT JOIN dates 
    ON appointments.appointment_date = dates.full_date







