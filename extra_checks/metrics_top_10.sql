SELECT TOP (10)
    event_id,
    hostname,
    event_timestamp,
    cpu_usage_percent,
    memory_usage_percent,
    ingested_at
FROM dbo.system_metrics
ORDER BY ingested_at DESC;