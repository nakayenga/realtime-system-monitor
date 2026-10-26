CREATE INDEX IX_system_metrics_host_timestamp

ON dbo.system_metrics
(
    host_id,
    event_timestamp DESC
);
GO


CREATE INDEX IX_system_metrics_timestamp

ON dbo.system_metrics
(
    event_timestamp DESC
);
GO