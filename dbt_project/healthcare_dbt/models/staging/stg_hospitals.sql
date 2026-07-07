SELECT
    hospital_id,
    hospital_name,
    INITCAP(location) AS location,
    INITCAP(hospital_type) AS hospital_type
FROM {{ source('staging', 'hospitals') }}
