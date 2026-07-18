CREATE SCHEMA IF NOT EXISTS metadata;

CREATE TABLE IF NOT EXISTS metadata.pipeline_audit
(
    audit_id SERIAL PRIMARY KEY,

    pipeline_name VARCHAR(100) NOT NULL,

    airflow_run_id VARCHAR(200),

    run_start TIMESTAMP NOT NULL,

    run_end TIMESTAMP NOT NULL,

    duration_seconds NUMERIC(10,2),

    status VARCHAR(20) NOT NULL,

    rows_loaded INTEGER DEFAULT 0,

    dbt_models INTEGER DEFAULT 0,

    tests_total INTEGER DEFAULT 0,

    tests_passed INTEGER DEFAULT 0,

    tests_failed INTEGER DEFAULT 0,

    message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);