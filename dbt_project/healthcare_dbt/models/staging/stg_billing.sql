SELECT
    billing_id,
    appointment_id,
    billing_amount,
    insurance_covered,
    payment_status,
    payment_date
FROM {{ source('staging', 'billing') }}
