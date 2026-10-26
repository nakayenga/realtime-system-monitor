SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT event_id) AS unique_events,
    MIN(event_timestamp) AS first_event,
    MAX(event_timestamp) AS latest_event,
    MAX(ingested_at) AS latest_ingestion
FROM dbo.system_metrics;