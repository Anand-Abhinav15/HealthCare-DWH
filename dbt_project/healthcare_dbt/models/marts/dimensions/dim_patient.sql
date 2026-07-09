WITH patients AS (
    SELECT *
    FROM {{ ref('stg_patients')}}
)

SELECT 
    {{ dbt_utils.generate_surrogate_key(['patient_id']) }} AS patient_key,
    patient_id,
    patient_name,
    gender,
    age,
    age_group,
    city,
    insurance_provider,
    registration_date
FROM patients