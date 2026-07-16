CREATE SCHEMA IF NOT EXISTS metadata;

CREATE TABLE IF NOT EXISTS metadata.pipeline_audit (

    audit_id SERIAL PRIMARY KEY,

    pipeline_name VARCHAR(100),

    run_start TIMESTAMP,

    run_end TIMESTAMP,

    status VARCHAR(20),

    rows_loaded INTEGER,

    duration_seconds NUMERIC(10,2),

    message TEXT

);