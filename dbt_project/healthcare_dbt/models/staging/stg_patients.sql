SELECT
    patient_id,
    first_name,
    last_name,
    gender,
    date_of_birth,
    city,
    insurance_provider,
    registration_date
FROM {{ source('staging', 'patients') }}