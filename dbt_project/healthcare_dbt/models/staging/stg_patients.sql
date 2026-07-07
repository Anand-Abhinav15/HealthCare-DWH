WITH source AS (
    SELECT *
    FROM {{ source('staging', 'patients') }}
),

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
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, CAST(date_of_birth AS DATE)))::INT AS age
    FROM source
),

final AS (
    SELECT
        *,
        CASE
            WHEN age < 18 THEN 'Child'
            WHEN age BETWEEN 18 AND 35 THEN 'Young Adult'
            WHEN age BETWEEN 36 AND 60 THEN 'Adult'
            ELSE 'Senior'
        END AS age_group
    FROM cleaned
)


SELECT *
FROM final

