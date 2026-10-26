import json
import os
import time
import uuid

from datetime import (
    datetime,
    timezone,
)

from confluent_kafka import (
    Producer,
)


BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)

TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "system-metrics",
)

TOTAL_EVENTS = int(
    os.getenv(
        "LOAD_TEST_EVENTS",
        "100000",
    )
)


producer = Producer(
    {
        "bootstrap.servers":
            BOOTSTRAP_SERVERS,

        "acks":
            "all",

        "enable.idempotence":
            True,

        "compression.type":
            "lz4",

        "linger.ms":
            10,
    }
)


start = time.perf_counter()


for index in range(
    TOTAL_EVENTS
):

    host_id = (
        f"load-host-{index % 100}"
    )

    event = {
        "event_id":
            str(uuid.uuid4()),

        "host_id":
            host_id,

        "event_timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "sequence":
            index,
    }

    while True:

        try:
            producer.produce(
                TOPIC,

                key=host_id.encode(
                    "utf-8"
                ),

                value=json.dumps(
                    event
                ).encode(
                    "utf-8"
                ),
            )

            break

        except BufferError:
            producer.poll(
                0.1
            )

    producer.poll(0)


producer.flush()


elapsed = (
    time.perf_counter()
    - start
)


print(
    f"Events: {TOTAL_EVENTS:,}"
)

print(
    f"Elapsed: {elapsed:.2f}s"
)

print(
    "Producer throughput: "
    f"{TOTAL_EVENTS / elapsed:,.0f} events/sec"
)