SELECT
    hospital_id,
    hospital_name,
    location,
    hospital_type
FROM {{ source('staging', 'hospitals') }}
