WITH hospitals AS (
    SELECT *
    FROM {{ ref('stg_hospitals')}}
)

SELECT 
    {{ dbt_utils.generate_surrogate_key(['hospital_id']) }} AS hospital_key,
    hospital_id,
    hospital_name,
    location,
    hospital_type
FROM hospitals