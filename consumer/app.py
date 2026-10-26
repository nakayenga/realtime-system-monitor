
import logging
import time

from confluent_kafka import TopicPartition
from prometheus_client import start_http_server

from consumer.config import (
    BATCH_SIZE,
    FLUSH_INTERVAL_SECONDS,
    KAFKA_TOPIC,
)
from consumer.database import (
    create_connection,
    insert_batch,
)
from consumer.dlq import send_to_dlq
from consumer.health import (
    mark_ready,
    start_health_server,
)
from consumer.kafka_client import create_consumer
from consumer.logging_config import configure_logging
from consumer.models import MetricEvent
from consumer.observability import (
    BATCH_SIZE_METRIC,
    DATABASE_WRITE_SECONDS,
    DLQ_EVENTS,
    EVENTS_FAILED,
    EVENTS_PROCESSED,
    EVENTS_RECEIVED,
)
from consumer.transformer import transform


logger = logging.getLogger(__name__)


def message_commit_offset(message):
    # Kafka commits the NEXT offset to consume.
    return TopicPartition(
        message.topic(),
        message.partition(),
        message.offset() + 1,
    )



def commit_offsets(consumer, offsets):
    if not offsets:
        return

    partitions = [
        TopicPartition(topic, partition, offset)
        for (topic, partition), offset in offsets.items()
    ]

    results = consumer.commit(
        offsets=partitions,
        asynchronous=False,
    )

    if results is None:
        raise RuntimeError(
            "Kafka offset commit returned no result"
        )

    for result in results:
        if result.error is not None:
            raise RuntimeError(
                f"Kafka offset commit failed: {result.error}"
            )



def flush_batch(connection, consumer, batch, offsets):
    if not batch:
        return

    BATCH_SIZE_METRIC.set(len(batch))

    with DATABASE_WRITE_SECONDS.time():
        insert_batch(connection, batch)

    # SQL has committed successfully.
    # Commit only offsets represented by this batch.
    commit_offsets(consumer, offsets)

    EVENTS_PROCESSED.inc(len(batch))

    logger.info(
        "Inserted batch size=%s",
        len(batch),
    )

    batch.clear()
    offsets.clear()
    BATCH_SIZE_METRIC.set(0)


def main():
    configure_logging()

    start_health_server()
    start_http_server(8000)

    consumer = None
    connection = None

    batch = []
    offsets = {}

    last_flush = time.monotonic()
    shutting_down_normally = False

    try:
        consumer = create_consumer()
        connection = create_connection()

        consumer.subscribe([KAFKA_TOPIC])

        mark_ready()
        logger.info("Consumer started")

        while True:
            message = consumer.poll(1.0)

            if message is not None:
                if message.error():
                    raise RuntimeError(
                        f"Kafka consumer error: {message.error()}"
                    )

                EVENTS_RECEIVED.inc()

                try:
                    event = MetricEvent.model_validate_json(
                        message.value()
                    )
                    record = transform(event)

                except Exception as exc:
                    EVENTS_FAILED.inc()

                    logger.exception(
                        "Event validation or transformation failed"
                    )

                    # Persist preceding valid records before
                    # acknowledging a later invalid message.
                    flush_batch(
                        connection,
                        consumer,
                        batch,
                        offsets,
                    )

                    # If delivery fails, do not commit this offset.
                    send_to_dlq(message, exc)
                    DLQ_EVENTS.inc()

                    offset = message_commit_offset(message)

                    commit_offsets(
                        consumer,
                        {
                            (offset.topic, offset.partition):
                                offset.offset
                        },
                    )

                    last_flush = time.monotonic()

                else:
                    batch.append(record)

                    offset = message_commit_offset(message)
                    key = (offset.topic, offset.partition)

                    offsets[key] = max(
                        offsets.get(key, 0),
                        offset.offset,
                    )

            BATCH_SIZE_METRIC.set(len(batch))

            now = time.monotonic()

            batch_full = len(batch) >= BATCH_SIZE

            timer_expired = (
                bool(batch)
                and now - last_flush >= FLUSH_INTERVAL_SECONDS
            )

            if batch_full or timer_expired:
                flush_batch(
                    connection,
                    consumer,
                    batch,
                    offsets,
                )
                last_flush = time.monotonic()

    except KeyboardInterrupt:
        logger.info("Consumer shutting down")
        shutting_down_normally = True

    except Exception:
        logger.exception(
            "Consumer stopped because of an error"
        )
        raise

    finally:
        try:
            # Only flush remaining records on normal shutdown.
            # After an error, leave uncommitted records for replay.
            if (
                shutting_down_normally
                and batch
                and connection is not None
                and consumer is not None
            ):
                flush_batch(
                    connection,
                    consumer,
                    batch,
                    offsets,
                )
        finally:
            if consumer is not None:
                consumer.close()

            if connection is not None:
                connection.close()


if __name__ == "__main__":
    main()
