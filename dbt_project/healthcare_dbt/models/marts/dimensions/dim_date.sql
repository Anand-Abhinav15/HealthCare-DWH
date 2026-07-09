WITH dates AS (
    SELECT
        generate_series(
            DATE '2022-01-01',
            DATE '2030-12-31',
            INTERVAL '1 day'
        )::date AS full_date
)

SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::INTEGER AS date_key,
    full_date,
    EXTRACT(DAY FROM full_date)::INT AS day,
    EXTRACT(MONTH FROM full_date)::INT AS month,
    TO_CHAR(full_date, 'Month') AS month_name,
    EXTRACT(QUARTER FROM full_date)::INT AS quarter,
    EXTRACT(YEAR FROM full_date)::INT AS year,
    TO_CHAR(full_date, 'Day') AS weekday,
    CASE
        WHEN EXTRACT(ISODOW FROM full_date) IN (6,7)
        THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM dates



