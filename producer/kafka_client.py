
import logging

from confluent_kafka import Producer

from producer.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_SASL_MECHANISM,
    KAFKA_SASL_PASSWORD,
    KAFKA_SASL_USERNAME,
    KAFKA_SECURITY_PROTOCOL,
)


logger = logging.getLogger(__name__)


def build_kafka_config():
    config = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "security.protocol": KAFKA_SECURITY_PROTOCOL,

        "acks": "all",
        "enable.idempotence": False,

        # Disable compression for the first
        # Azure Event Hubs connectivity test.
        "compression.type": "none",

        "linger.ms": 10,
        "retries": 10,
        "request.timeout.ms": 60000,
    }

    if KAFKA_SASL_USERNAME:
        config.update(
            {
                "sasl.mechanism": KAFKA_SASL_MECHANISM,
                "sasl.username": KAFKA_SASL_USERNAME,
                "sasl.password": KAFKA_SASL_PASSWORD,
            }
        )

    return config


def create_producer():
    return Producer(build_kafka_config())


def delivery_report(error, message):
    if error is not None:
        logger.error(
            "Kafka delivery failed: %s",
            error,
        )
        return

    logger.info(
        "Event delivered successfully: "
        "topic=%s partition=%s offset=%s",
        message.topic(),
        message.partition(),
        message.offset(),
    )


def publish_event(producer, topic, event):
    producer.produce(
        topic=topic,

        # Same host -> same Kafka partition.
        key=event.host_id.encode("utf-8"),

        value=event.model_dump_json().encode("utf-8"),

        callback=delivery_report,
    )

    # Process available delivery callbacks.
    producer.poll(0)
