from confluent_kafka import Consumer

from consumer.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_GROUP,
    KAFKA_SASL_MECHANISM,
    KAFKA_SASL_PASSWORD,
    KAFKA_SASL_USERNAME,
    KAFKA_SECURITY_PROTOCOL,
)


def build_consumer_config():
    config = {
        "bootstrap.servers":
            KAFKA_BOOTSTRAP_SERVERS,

        "group.id":
            KAFKA_GROUP,

        "auto.offset.reset":
            "earliest",

        "enable.auto.commit":
            False,

        "security.protocol":
            KAFKA_SECURITY_PROTOCOL,
    }

    if KAFKA_SASL_USERNAME:
        config.update(
            {
                "sasl.mechanism":
                    KAFKA_SASL_MECHANISM,

                "sasl.username":
                    KAFKA_SASL_USERNAME,

                "sasl.password":
                    KAFKA_SASL_PASSWORD,
            }
        )

    return config


def create_consumer():
    return Consumer(
        build_consumer_config()
    )