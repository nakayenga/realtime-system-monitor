from datetime import datetime

from pydantic import BaseModel, Field


class CpuMetrics(BaseModel):
    usage_percent: float = Field(ge=0, le=100)
    user_percent: float = Field(ge=0, le=100)
    system_percent: float = Field(ge=0, le=100)
    idle_percent: float = Field(ge=0, le=100)

    logical_cores: int | None = Field(default=None, ge=1)
    physical_cores: int | None = Field(default=None, ge=1)

    context_switches: int = Field(ge=0)
    interrupts: int = Field(ge=0)
    software_interrupts: int = Field(ge=0)


class MemoryMetrics(BaseModel):
    total_bytes: int = Field(ge=0)
    available_bytes: int = Field(ge=0)
    used_bytes: int = Field(ge=0)
    free_bytes: int = Field(ge=0)
    usage_percent: float = Field(ge=0, le=100)


class DiskMetrics(BaseModel):
    total_bytes: int = Field(ge=0)
    used_bytes: int = Field(ge=0)
    free_bytes: int = Field(ge=0)
    usage_percent: float = Field(ge=0, le=100)

    read_count: int | None = Field(default=None, ge=0)
    write_count: int | None = Field(default=None, ge=0)
    read_bytes: int | None = Field(default=None, ge=0)
    write_bytes: int | None = Field(default=None, ge=0)


class NetworkMetrics(BaseModel):
    bytes_sent: int = Field(ge=0)
    bytes_received: int = Field(ge=0)

    packets_sent: int = Field(ge=0)
    packets_received: int = Field(ge=0)

    errors_in: int = Field(ge=0)
    errors_out: int = Field(ge=0)

    dropped_in: int = Field(ge=0)
    dropped_out: int = Field(ge=0)


class MetricEvent(BaseModel):
    schema_version: int = 1

    event_id: str
    host_id: str
    hostname: str
    platform: str

    event_timestamp: datetime

    cpu: CpuMetrics
    memory: MemoryMetrics
    disk: DiskMetrics
    network: NetworkMetrics