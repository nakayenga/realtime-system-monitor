from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
)


EVENTS_RECEIVED = Counter(
    "metrics_events_received_total",
    "Events received from Kafka",
)


EVENTS_PROCESSED = Counter(
    "metrics_events_processed_total",
    "Events successfully processed",
)


EVENTS_FAILED = Counter(
    "metrics_events_failed_total",
    "Events that failed processing",
)


DLQ_EVENTS = Counter(
    "metrics_dlq_events_total",
    "Events sent to DLQ",
)


BATCH_SIZE_METRIC = Gauge(
    "metrics_current_batch_size",
    "Current database batch size",
)


DATABASE_WRITE_SECONDS = Histogram(
    "metrics_database_write_seconds",
    "Time spent writing database batches",
)