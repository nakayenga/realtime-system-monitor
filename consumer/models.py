from datetime import datetime

from pydantic import BaseModel, Field


class CpuMetrics(BaseModel):
    usage_percent: float = Field(ge=0, le=100)
    user_percent: float = Field(ge=0, le=100)
    system_percent: float = Field(ge=0, le=100)
    idle_percent: float = Field(ge=0, le=100)

    logical_cores: int | None = None
    physical_cores: int | None = None

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

    read_count: int | None = None
    write_count: int | None = None
    read_bytes: int | None = None
    write_bytes: int | None = None


class NetworkMetrics(BaseModel):
    bytes_sent: int
    bytes_received: int

    packets_sent: int
    packets_received: int

    errors_in: int
    errors_out: int

    dropped_in: int
    dropped_out: int


class MetricEvent(BaseModel):
    schema_version: int

    event_id: str
    host_id: str
    hostname: str
    platform: str

    event_timestamp: datetime

    cpu: CpuMetrics
    memory: MemoryMetrics
    disk: DiskMetrics
    network: NetworkMetrics