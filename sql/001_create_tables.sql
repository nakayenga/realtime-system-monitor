CREATE TABLE dbo.system_metrics
(
    metric_id BIGINT IDENTITY(1,1) NOT NULL,

    event_id UNIQUEIDENTIFIER NOT NULL,

    host_id VARCHAR(128) NOT NULL,

    hostname VARCHAR(255) NULL,

    platform VARCHAR(50) NULL,

    event_timestamp DATETIME2(3) NOT NULL,

    cpu_usage_percent FLOAT NULL,
    cpu_user_percent FLOAT NULL,
    cpu_system_percent FLOAT NULL,
    cpu_idle_percent FLOAT NULL,

    logical_cores INT NULL,
    physical_cores INT NULL,

    cpu_context_switches BIGINT NULL,
    cpu_interrupts BIGINT NULL,
    cpu_software_interrupts BIGINT NULL,

    memory_total_bytes BIGINT NULL,
    memory_available_bytes BIGINT NULL,
    memory_used_bytes BIGINT NULL,
    memory_free_bytes BIGINT NULL,
    memory_usage_percent FLOAT NULL,

    disk_total_bytes BIGINT NULL,
    disk_used_bytes BIGINT NULL,
    disk_free_bytes BIGINT NULL,
    disk_usage_percent FLOAT NULL,

    disk_read_count BIGINT NULL,
    disk_write_count BIGINT NULL,
    disk_read_bytes BIGINT NULL,
    disk_write_bytes BIGINT NULL,

    network_bytes_sent BIGINT NULL,
    network_bytes_received BIGINT NULL,

    network_packets_sent BIGINT NULL,
    network_packets_received BIGINT NULL,

    network_errors_in BIGINT NULL,
    network_errors_out BIGINT NULL,

    network_dropped_in BIGINT NULL,
    network_dropped_out BIGINT NULL,

    ingested_at DATETIME2(3)
        NOT NULL
        DEFAULT SYSUTCDATETIME(),

    CONSTRAINT PK_system_metrics
        PRIMARY KEY CLUSTERED(metric_id),

    CONSTRAINT UQ_system_metrics_event_id
        UNIQUE(event_id)
);
GO