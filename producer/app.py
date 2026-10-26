import logging
import time

from producer.config import (
    COLLECTION_INTERVAL_SECONDS,
    KAFKA_TOPIC,
)

from producer.kafka_client import (
    create_producer,
    publish_event,
)

from producer.logging_config import (
    configure_logging,
)

from producer.metrics import (
    collect_metrics,
)


logger = logging.getLogger(__name__)


def main():
    configure_logging()

    logger.info(
        "Starting metrics producer"
    )

    producer = create_producer()

    try:
        while True:
            event = collect_metrics()

            publish_event(
                producer,
                KAFKA_TOPIC,
                event,
            )

            logger.info(
                "Published metric event %s for host %s",
                event.event_id,
                event.host_id,
            )

            time.sleep(
                COLLECTION_INTERVAL_SECONDS
            )

    except KeyboardInterrupt:
        logger.info(
            "Producer shutting down"
        )

    finally:
        producer.flush(10)


if __name__ == "__main__":
    main()