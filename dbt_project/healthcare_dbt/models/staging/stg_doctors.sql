SELECT
    doctor_id,
    doctor_name,
    specialization,
    experience_years
FROM {{ source('staging', 'doctors') }}
