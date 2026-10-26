import json
import logging

from confluent_kafka import Producer

from consumer.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_DLQ_TOPIC,
    KAFKA_SASL_MECHANISM,
    KAFKA_SASL_PASSWORD,
    KAFKA_SASL_USERNAME,
    KAFKA_SECURITY_PROTOCOL,
)


logger = logging.getLogger(__name__)


def build_dlq_config():
    config = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "security.protocol": KAFKA_SECURITY_PROTOCOL,
        "acks": "all",
        "enable.idempotence": False,
        "compression.type": "none",
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


dlq_producer = Producer(build_dlq_config())


def send_to_dlq(message, error):
    payload = {
        "original_topic": message.topic(),
        "original_partition": message.partition(),
        "original_offset": message.offset(),
        "original_key": (
            message.key().decode(
                "utf-8",
                errors="replace",
            )
            if message.key() is not None
            else None
        ),
        "original_value": (
            message.value().decode(
                "utf-8",
                errors="replace",
            )
            if message.value() is not None
            else None
        ),
        "error_type": type(error).__name__,
        "error": str(error),
    }

    delivery = {
        "confirmed": False,
        "error": None,
    }

    def on_delivery(err, delivered_message):
        if err is not None:
            delivery["error"] = err
        else:
            delivery["confirmed"] = True

    dlq_producer.produce(
        KAFKA_DLQ_TOPIC,
        value=json.dumps(payload).encode("utf-8"),
        on_delivery=on_delivery,
    )

    remaining = dlq_producer.flush(10)

    if remaining != 0:
        raise RuntimeError(
            "DLQ delivery timed out; message not confirmed"
        )

    if delivery["error"] is not None:
        raise RuntimeError(
            f"DLQ delivery failed: {delivery['error']}"
        )

    if not delivery["confirmed"]:
        raise RuntimeError(
            "DLQ delivery acknowledgement missing"
        )

    logger.warning(
        "Message delivered to DLQ: "
        "topic=%s partition=%s offset=%s",
        message.topic(),
        message.partition(),
        message.offset(),
    )
