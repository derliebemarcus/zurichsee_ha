"""Base entity for Zurichsee Wetterstationen."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, STATION_NAMES
from .coordinator import ZurichseeCoordinator


class ZurichseeEntity(CoordinatorEntity[ZurichseeCoordinator]):
    """Base entity for Zurichsee Wetterstationen."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ZurichseeCoordinator,
        station_id: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._station_id = station_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, station_id)},
            name=STATION_NAMES.get(station_id, station_id),
            manufacturer="Stadt Zürich / Wasserschutzpolizei",
            model="Tecson Meteo Station",
            configuration_url=f"https://www.tecson-data.ch/zurich/{station_id}/",
        )
