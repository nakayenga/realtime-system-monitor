import os

from dotenv import load_dotenv


load_dotenv()


HOST_ID = os.getenv("HOST_ID")

COLLECTION_INTERVAL_SECONDS = float(
    os.getenv(
        "COLLECTION_INTERVAL_SECONDS",
        "5",
    )
)

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "system-metrics",
)

KAFKA_SECURITY_PROTOCOL = os.getenv(
    "KAFKA_SECURITY_PROTOCOL",
    "PLAINTEXT",
)

KAFKA_SASL_MECHANISM = os.getenv(
    "KAFKA_SASL_MECHANISM",
)

KAFKA_SASL_USERNAME = os.getenv(
    "KAFKA_SASL_USERNAME",
)

KAFKA_SASL_PASSWORD = os.getenv(
    "KAFKA_SASL_PASSWORD",
)