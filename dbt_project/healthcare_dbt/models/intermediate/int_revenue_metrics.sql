WITH fact AS (
    SELECT *
    FROM {{ ref('fact_appointments' )}}
),

dates AS (
    SELECT *
    FROM {{ ref('dim_date') }}
)

SELECT 
    d.year,
    d.quarter,
    d.month,
    TRIM(d.month_name) AS month_name,
    COUNT(f.appointment_id) AS total_appointments,
    SUM(f.billing_amount) AS total_revenue,
    SUM(f.treatment_cost) AS total_treatment_cost,
    AVG(f.billing_amount) AS avg_billing_amount,
    AVG(f.treatment_cost) AS avg_treatment_cost
FROM fact f
JOIN dates d
ON f.date_key = d.date_key
GROUP BY d.year, d.quarter, d.month, TRIM(d.month_name)
ORDER BY d.year, d.month








