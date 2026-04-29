"""DataUpdateCoordinator for Zurichsee Wetterstationen."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ZurichseeApiClient
from .exceptions import ZurichseeApiError
from .models import MeasurementData

LOGGER = logging.getLogger(__name__)


class ZurichseeCoordinator(DataUpdateCoordinator[dict[str, MeasurementData]]):
    """Class to manage fetching Zurichsee data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: ZurichseeApiClient,
        stations: list[str],
        update_interval: int,
    ) -> None:
        """Initialize."""
        self._api = api
        self._stations = stations

        super().__init__(
            hass,
            LOGGER,
            name="Zurichsee Wetterstationen",
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self) -> dict[str, MeasurementData]:
        """Update data via library."""
        data: dict[str, MeasurementData] = {}
        for station in self._stations:
            try:
                result = await self._api.async_get_measurements(station)
                if result:
                    data[station] = result
            except ZurichseeApiError as err:
                raise UpdateFailed(f"Error communicating with API for {station}: {err}") from err

        return data
