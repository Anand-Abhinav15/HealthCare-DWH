SELECT
    bill_id as billing_id,
    appointment_id,
    billing_amount,
    insurance_covered,
    payment_status,
    payment_date,
    CASE
        WHEN insurance_covered THEN billing_amount*0.8
        ELSE 0
    END AS insurance_coverage_amount
FROM {{ source('staging', 'billing') }}
