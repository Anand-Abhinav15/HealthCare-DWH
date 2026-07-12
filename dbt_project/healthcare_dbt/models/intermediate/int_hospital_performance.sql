WITH fact AS (
    SELECT *
    FROM {{ ref('fact_appointments') }}
),

hospitals AS (
    SELECT *
    FROM {{ ref('dim_hospital') }}
)

SELECT
    h.hospital_key,
    h.hospital_name,
    h.location,
    h.hospital_type,
    COUNT(f.appointment_id) AS total_appointments,
    SUM(f.billing_amount) AS total_revenue,
    AVG(f.treatment_cost) AS avg_treatment_cost,
    AVG(f.appointment_duration) AS avg_appointment_duration
FROM hospitals h
LEFT JOIN fact f
ON h.hospital_key = f.hospital_key
GROUP BY h.hospital_key, h.hospital_name, h.location, h.hospital_type