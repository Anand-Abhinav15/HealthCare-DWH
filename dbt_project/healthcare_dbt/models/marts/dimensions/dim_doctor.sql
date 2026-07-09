WITH doctors AS (
    SELECT *
    FROM {{ ref('stg_doctors')}}
)

SELECT 
    {{ dbt_utils.generate_surrogate_key(['doctor_id']) }} AS doctor_key,
    doctor_id,
    doctor_name,
    specialization,
    experience_level,
    experience_years
FROM doctors