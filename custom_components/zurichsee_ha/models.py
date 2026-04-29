"""Models for the Zurichsee Wetterstationen integration."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ValueEntry(BaseModel):
    """A single value entry with unit and status."""

    value: Any = Field(default=None)
    unit: str = Field(default="")
    status: str = Field(default="")


class MeasurementEntry(BaseModel):
    """A single measurement entry for a station."""

    station: str
    timestamp: datetime
    values: dict[str, ValueEntry] = Field(default_factory=dict)


class MeasurementResponse(BaseModel):
    """API response envelope."""

    ok: bool = Field(default=True)
    result: list[MeasurementEntry] = Field(default_factory=list)


class MeasurementData(BaseModel):
    """Flattened measurement data for the integration."""

    air_temperature: float | None = None
    water_temperature: float | None = None
    wind_direction: float | None = None
    wind_force_avg_10min: float | None = None
    wind_gust_max_10min: float | None = None
    wind_speed_avg_10min: float | None = None
    windchill: float | None = None
    barometric_pressure_qfe: float | None = None
    dew_point: float | None = None
    humidity: float | None = None
    precipitation: float | None = None
    global_radiation: float | None = None
    water_level: float | None = None
    timestamp_cet: datetime | None = None
