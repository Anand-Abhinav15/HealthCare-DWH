{% snapshot patient_snapshot %}

{{
    config(
        target_schema= 'snapshots',
        unique_key= 'patient_id',
        strategy= 'check',
        check_cols= [
            'city',
            'insurance_provider'
        ]
    )
}}

SELECT
    patient_id,
    patient_name,
    gender,
    age,
    age_group,
    city,
    insurance_provider,
    registration_date
FROM {{ ref('stg_patients') }}

{% endsnapshot %}

