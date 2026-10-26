from consumer.models import MetricEvent


def transform(
    event: MetricEvent,
) -> tuple:

    return (
        event.event_id,
        event.host_id,
        event.hostname,
        event.platform,
        event.event_timestamp,

        event.cpu.usage_percent,
        event.cpu.user_percent,
        event.cpu.system_percent,
        event.cpu.idle_percent,

        event.cpu.logical_cores,
        event.cpu.physical_cores,

        event.cpu.context_switches,
        event.cpu.interrupts,
        event.cpu.software_interrupts,

        event.memory.total_bytes,
        event.memory.available_bytes,
        event.memory.used_bytes,
        event.memory.free_bytes,
        event.memory.usage_percent,

        event.disk.total_bytes,
        event.disk.used_bytes,
        event.disk.free_bytes,
        event.disk.usage_percent,

        event.disk.read_count,
        event.disk.write_count,
        event.disk.read_bytes,
        event.disk.write_bytes,

        event.network.bytes_sent,
        event.network.bytes_received,

        event.network.packets_sent,
        event.network.packets_received,

        event.network.errors_in,
        event.network.errors_out,

        event.network.dropped_in,
        event.network.dropped_out,
    )