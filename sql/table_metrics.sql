CREATE TABLE IF NOT EXISTS metadata.table_load_metrics (

    metric_id SERIAL PRIMARY KEY,

    pipeline_name TEXT,

    table_name TEXT,

    rows_loaded INTEGER,

    load_duration_seconds NUMERIC(10,2),

    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);