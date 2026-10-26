import os

from dotenv import load_dotenv


load_dotenv()


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "system-metrics",
)

KAFKA_DLQ_TOPIC = os.getenv(
    "KAFKA_DLQ_TOPIC",
    "system-metrics-dlq",
)

KAFKA_GROUP = os.getenv(
    "KAFKA_GROUP",
    "metrics-sql-writers",
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

SQL_CONNECTION_STRING = os.getenv(
    "SQL_CONNECTION_STRING"
)

BATCH_SIZE = int(
    os.getenv(
        "BATCH_SIZE",
        "250",
    )
)

FLUSH_INTERVAL_SECONDS = float(
    os.getenv(
        "FLUSH_INTERVAL_SECONDS",
        "2",
    )
)