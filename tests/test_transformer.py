from datetime import datetime, timezone

from consumer.models import (
    CpuMetrics,
    DiskMetrics,
    MemoryMetrics,
    MetricEvent,
    NetworkMetrics,
)

from consumer.transformer import (
    transform,
)


def test_transform():
    event = MetricEvent(
        schema_version=1,

        event_id="00000000-0000-0000-0000-000000000001",

        host_id="test-host",

        hostname="test-host",

        platform="Windows",

        event_timestamp=datetime.now(
            timezone.utc
        ),

        cpu=CpuMetrics(
            usage_percent=20,
            user_percent=10,
            system_percent=5,
            idle_percent=65,
            logical_cores=8,
            physical_cores=4,
            context_switches=100,
            interrupts=200,
            software_interrupts=0,
        ),

        memory=MemoryMetrics(
            total_bytes=1000,
            available_bytes=500,
            used_bytes=500,
            free_bytes=500,
            usage_percent=50,
        ),

        disk=DiskMetrics(
            total_bytes=1000,
            used_bytes=400,
            free_bytes=600,
            usage_percent=40,
            read_count=10,
            write_count=20,
            read_bytes=100,
            write_bytes=200,
        ),

        network=NetworkMetrics(
            bytes_sent=100,
            bytes_received=200,
            packets_sent=10,
            packets_received=20,
            errors_in=0,
            errors_out=0,
            dropped_in=0,
            dropped_out=0,
        ),
    )

    result = transform(event)

    assert result[0] == event.event_id

    assert result[1] == "test-host"

    assert result[5] == 20