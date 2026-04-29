"""Sensor platform for Zurichsee Wetterstationen."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfLength,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import CONF_STATIONS, DEFAULT_OPTIONS
from .coordinator import ZurichseeCoordinator
from .entity import ZurichseeEntity

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ZurichseeSensorEntityDescription(SensorEntityDescription):
    """Class describing Zurichsee sensor entities."""


SENSOR_DESCRIPTIONS: tuple[ZurichseeSensorEntityDescription, ...] = (
    ZurichseeSensorEntityDescription(
        key="air_temperature",
        translation_key="air_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    ZurichseeSensorEntityDescription(
        key="water_temperature",
        translation_key="water_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    ZurichseeSensorEntityDescription(
        key="wind_speed_avg_10min",
        translation_key="wind_speed_avg_10min",
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfSpeed.METERS_PER_SECOND,
        suggested_display_precision=1,
    ),
    ZurichseeSensorEntityDescription(
        key="wind_gust_max_10min",
        translation_key="wind_gust_max_10min",
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfSpeed.METERS_PER_SECOND,
        suggested_display_precision=1,
    ),
    ZurichseeSensorEntityDescription(
        key="wind_direction",
        translation_key="wind_direction",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="°",
        suggested_display_precision=0,
    ),
    ZurichseeSensorEntityDescription(
        key="wind_force_avg_10min",
        translation_key="wind_force_avg_10min",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="Bft",
        suggested_display_precision=0,
    ),
    ZurichseeSensorEntityDescription(
        key="windchill",
        translation_key="windchill",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    ZurichseeSensorEntityDescription(
        key="humidity",
        translation_key="humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=0,
    ),
    ZurichseeSensorEntityDescription(
        key="dew_point",
        translation_key="dew_point",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
    ),
    ZurichseeSensorEntityDescription(
        key="barometric_pressure_qfe",
        translation_key="barometric_pressure_qfe",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.HPA,
        suggested_display_precision=1,
    ),
    ZurichseeSensorEntityDescription(
        key="precipitation",
        translation_key="precipitation",
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="mm",
        suggested_display_precision=1,
    ),
    ZurichseeSensorEntityDescription(
        key="global_radiation",
        translation_key="global_radiation",
        device_class=SensorDeviceClass.IRRADIANCE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="W/m²",
        suggested_display_precision=1,
    ),
    ZurichseeSensorEntityDescription(
        key="water_level",
        translation_key="water_level",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfLength.METERS,
        suggested_display_precision=2,
    ),
    ZurichseeSensorEntityDescription(
        key="timestamp_cet",
        translation_key="timestamp_cet",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: ZurichseeCoordinator = entry.runtime_data
    stations = entry.options.get(CONF_STATIONS, DEFAULT_OPTIONS[CONF_STATIONS])

    entities: list[ZurichseeSensor] = []

    for station_id in stations:
        for description in SENSOR_DESCRIPTIONS:
            entities.append(ZurichseeSensor(coordinator, station_id, description))

    async_add_entities(entities)


class ZurichseeSensor(ZurichseeEntity, SensorEntity):
    """Sensor for Zurichsee Wetterstationen."""

    entity_description: ZurichseeSensorEntityDescription

    def __init__(
        self,
        coordinator: ZurichseeCoordinator,
        station_id: str,
        description: ZurichseeSensorEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, station_id)
        self.entity_description = description
        self._attr_unique_id = f"{station_id}_{description.key}"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data or self._station_id not in self.coordinator.data:
            return None

        data = self.coordinator.data[self._station_id]
        return getattr(data, self.entity_description.key, None)
