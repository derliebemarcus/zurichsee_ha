"""Models for the Zurichsee Wetterstationen integration."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class MeasurementValues(BaseModel):
    """Measurements for a single station."""

    air_temperature: float | None = Field(default=None)
    water_temperature: float | None = Field(default=None)
    wind_direction: float | None = Field(default=None)
    wind_force_avg_10min: float | None = Field(default=None)
    wind_gust_max_10min: float | None = Field(default=None)
    wind_speed_avg_10min: float | None = Field(default=None)
    barometric_pressure_qfe: float | None = Field(default=None)
    barometric_pressure_qff: float | None = Field(default=None)
    barometric_pressure_qnh: float | None = Field(default=None)
    dew_point: float | None = Field(default=None)
    humidity: float | None = Field(default=None)
    precipitation_mm: float | None = Field(default=None)
    precipitation_type: str | None = Field(default=None)
    global_radiation: float | None = Field(default=None)
    timestamp_cet: datetime | None = Field(default=None)

    @field_validator("timestamp_cet", mode="before")
    @classmethod
    def parse_timestamp(cls, value: Any) -> datetime | None:
        """Parse timestamp from string if needed."""
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None
        return value


class MeasurementResponse(BaseModel):
    """API response envelope."""

    ok: bool = Field(default=True)
    result: list[MeasurementValues] = Field(default_factory=list)
