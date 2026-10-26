from producer.metrics import (
    collect_metrics,
)


def test_complete_event():
    event = collect_metrics()

    assert event.schema_version == 1

    assert event.event_id

    assert event.host_id

    assert event.hostname

    assert event.event_timestamp

    assert 0 <= event.cpu.usage_percent <= 100

    assert 0 <= event.memory.usage_percent <= 100

    assert 0 <= event.disk.usage_percent <= 100

    assert event.network.bytes_sent >= 0

    assert event.network.bytes_received >= 0


def test_serialization():
    event = collect_metrics()

    payload = event.model_dump_json()

    assert isinstance(
        payload,
        str,
    )

    assert event.event_id in payload