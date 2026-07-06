SELECT
    appointment_id,
    patient_id,
    doctor_id,
    hospital_id,
    appointment_date,
    diagnosis_code,
    treatment_cost,
    appointment_duration,
    status
FROM {{ source('staging', 'appointments') }}
