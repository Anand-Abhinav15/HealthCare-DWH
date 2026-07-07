SELECT
    appointment_id,
    patient_id,
    doctor_id,
    hospital_id,
    appointment_date,
    EXTRACT(YEAR FROM appointment_date::DATE) AS appointment_year,
    EXTRACT(MONTH FROM appointment_date::DATE) AS appointment_month,
    TO_CHAR(appointment_date::DATE, 'Day') AS appointment_weekday,
    status = 'Completed' AS is_completed,
    diagnosis_code,
    treatment_cost,
    appointment_duration,
    status
FROM {{ source('staging', 'appointments') }}
