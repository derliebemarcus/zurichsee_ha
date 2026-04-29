"""API Client for Zurichsee Wetterstationen."""

from __future__ import annotations

import logging

import aiohttp
from yarl import URL

from .const import API_BASE_URL
from .exceptions import ZurichseeApiError
from .models import MeasurementResponse, MeasurementValues

LOGGER = logging.getLogger(__name__)


class ZurichseeApiClient:
    """API Client for fetching weather data from tecdottir."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the client."""
        self._session = session
        self._base_url = URL(API_BASE_URL)

    async def async_get_measurements(self, station: str) -> MeasurementValues | None:
        """Fetch the latest measurement for a specific station."""
        url = self._base_url / "measurements" / station
        params = {
            "limit": 1,
            "sort": "timestamp_cet desc",
        }

        try:
            async with self._session.get(url, params=params, timeout=20) as response:
                if response.status != 200:
                    raise ZurichseeApiError(
                        f"Failed to fetch data from {station}: {response.status}"
                    )

                data = await response.json()
                parsed = MeasurementResponse.model_validate(data)

                if not parsed.result:
                    return None

                return parsed.result[0]

        except TimeoutError as err:
            raise ZurichseeApiError(f"Timeout fetching data from {station}") from err
        except aiohttp.ClientError as err:
            raise ZurichseeApiError(f"Network error fetching data from {station}") from err
        except Exception as err:
            raise ZurichseeApiError(
                f"Unexpected error fetching data from {station}: {err}"
            ) from err

    async def async_validate_connection(self) -> None:
        """Validate connection by fetching a single station's data."""
        # We use mythenquai as a health check
        await self.async_get_measurements("mythenquai")
