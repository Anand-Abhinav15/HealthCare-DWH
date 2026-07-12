WITH fact AS (
    SELECT *
    FROM {{ ref('fact_appointments') }}
),

doctor AS (
    SELECT *
    FROM {{ ref('dim_doctor') }}
)

SELECT
    doctor.doctor_key,
    doctor.doctor_name,
    COUNT(*) AS appointments,
    SUM(treatment_cost) AS revenue,
    AVG(appointment_duration) AS avg_duration
FROM fact
JOIN doctor
ON fact.doctor_key = doctor.doctor_key
GROUP BY doctor.doctor_key, doctor.doctor_name