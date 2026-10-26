CREATE VIEW dbo.v_metrics_1minute
AS

SELECT
    host_id,

    DATEADD(
        MINUTE,

        DATEDIFF(
            MINUTE,
            0,
            event_timestamp
        ),

        0
    )
    AS metric_minute,

    AVG(cpu_usage_percent)
        AS avg_cpu_percent,

    MAX(cpu_usage_percent)
        AS max_cpu_percent,

    AVG(memory_usage_percent)
        AS avg_memory_percent,

    MAX(memory_usage_percent)
        AS max_memory_percent,

    AVG(disk_usage_percent)
        AS avg_disk_percent,

    MAX(disk_usage_percent)
        AS max_disk_percent,

    COUNT_BIG(*)
        AS sample_count

FROM dbo.system_metrics

GROUP BY
    host_id,

    DATEADD(
        MINUTE,

        DATEDIFF(
            MINUTE,
            0,
            event_timestamp
        ),

        0
    );
GO