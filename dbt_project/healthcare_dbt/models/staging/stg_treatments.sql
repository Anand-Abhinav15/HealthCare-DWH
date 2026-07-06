SELECT
    treatment_id,
    appointment_id,
    treatment_name,
    treatment_category
FROM {{ source('staging', 'treatments') }}