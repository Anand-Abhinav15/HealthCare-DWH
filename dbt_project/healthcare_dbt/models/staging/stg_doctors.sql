WITH source AS (
    SELECT *
    FROM {{ source('staging', 'doctors') }}
)


SELECT
    doctor_id,
    TRIM(doctor_name) AS doctor_name,
    INITCAP(specialization) AS specialization,
    experience_years,
    CASE
        WHEN experience_years < 5 THEN 'Junior'
        WHEN experience_years < 15 THEN 'Mid'
        ELSE 'Senior'
    END AS experience_level
FROM source
