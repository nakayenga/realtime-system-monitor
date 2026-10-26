SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT event_id) AS unique_events,
    MAX(ingested_at) AS latest_ingestion
FROM dbo.system_metrics;