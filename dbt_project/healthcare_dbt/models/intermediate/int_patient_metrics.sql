WITH fact AS (
    SELECT *
    FROM {{ ref('fact_appointments') }}
),

patients AS (
    SELECT *
    FROM {{ ref('dim_patient') }}
),

SELECT
    p.patient_key,
    p.patient_name,
    COUNT(f.appointment_id) AS total_appointments,
    SUM(f.billing_amount) AS total_spent,
    AVG(f.billing_amount) AS avg_spent,
    MIN(f.date_key) AS first_visit,
    MAX(f.date_key) AS last_visit
FROM patients p
LEFT JOIN fact f
ON p.patient_key = f.patient_key
GROUP BY p.patient_key, p.patient_name