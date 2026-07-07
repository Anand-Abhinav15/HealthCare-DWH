WITH source AS (
    SELECT *
    FROM {{ source('staging', 'patients') }}
);

cleaned AS (
    SELECT
        patient_id,
        TRIM(first_name) AS first_name,
        TRIM(last_name) AS last_name,
        CONCAT(TRIM(first_name), ' ',TRIM(last_name)) AS patient_name,
        LOWER(gender) AS gender,
        CAST(date_of_birth AS DATE) AS date_of_birth,
        CAST(registration_date AS DATE) AS registration_date,
        INITCAP(city) AS city,
        insurance_provider,
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth))::INT AS age
    FROM source
)


SELECT *
FROM cleaned

