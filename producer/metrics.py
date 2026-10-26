import os
import platform
import socket
import uuid

from datetime import datetime, timezone

import psutil

from producer.config import HOST_ID

from producer.models import (
    CpuMetrics,
    DiskMetrics,
    MemoryMetrics,
    MetricEvent,
    NetworkMetrics,
)


def get_host_id() -> str:
    return HOST_ID or socket.gethostname()


def get_disk_path() -> str:
    if os.name == "nt":
        return os.environ.get(
            "SystemDrive",
            "C:",
        ) + "\\"

    return "/"


def collect_cpu_metrics() -> CpuMetrics:
    usage = psutil.cpu_percent(
        interval=0.2
    )

    times = psutil.cpu_times_percent(
        interval=None
    )

    stats = psutil.cpu_stats()

    return CpuMetrics(
        usage_percent=usage,

        user_percent=getattr(
            times,
            "user",
            0.0,
        ),

        system_percent=getattr(
            times,
            "system",
            0.0,
        ),

        idle_percent=getattr(
            times,
            "idle",
            0.0,
        ),

        logical_cores=psutil.cpu_count(
            logical=True
        ),

        physical_cores=psutil.cpu_count(
            logical=False
        ),

        context_switches=stats.ctx_switches,

        interrupts=stats.interrupts,

        software_interrupts=stats.soft_interrupts,
    )


def collect_memory_metrics() -> MemoryMetrics:
    memory = psutil.virtual_memory()

    return MemoryMetrics(
        total_bytes=memory.total,
        available_bytes=memory.available,
        used_bytes=memory.used,
        free_bytes=memory.free,
        usage_percent=memory.percent,
    )


def collect_disk_metrics() -> DiskMetrics:
    usage = psutil.disk_usage(
        get_disk_path()
    )

    io = psutil.disk_io_counters()

    return DiskMetrics(
        total_bytes=usage.total,
        used_bytes=usage.used,
        free_bytes=usage.free,
        usage_percent=usage.percent,

        read_count=(
            io.read_count
            if io
            else None
        ),

        write_count=(
            io.write_count
            if io
            else None
        ),

        read_bytes=(
            io.read_bytes
            if io
            else None
        ),

        write_bytes=(
            io.write_bytes
            if io
            else None
        ),
    )


def collect_network_metrics() -> NetworkMetrics:
    network = psutil.net_io_counters()

    return NetworkMetrics(
        bytes_sent=network.bytes_sent,
        bytes_received=network.bytes_recv,

        packets_sent=network.packets_sent,
        packets_received=network.packets_recv,

        errors_in=network.errin,
        errors_out=network.errout,

        dropped_in=network.dropin,
        dropped_out=network.dropout,
    )


def collect_metrics() -> MetricEvent:
    return MetricEvent(
        schema_version=1,

        event_id=str(
            uuid.uuid4()
        ),

        host_id=get_host_id(),

        hostname=socket.gethostname(),

        platform=platform.system(),

        event_timestamp=datetime.now(
            timezone.utc
        ),

        cpu=collect_cpu_metrics(),

        memory=collect_memory_metrics(),

        disk=collect_disk_metrics(),

        network=collect_network_metrics(),
    )