"""API Client for Zurichsee Wetterstationen."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import aiohttp
from yarl import URL

from .const import API_BASE_URL
from .exceptions import ZurichseeApiError
from .models import MeasurementData, MeasurementResponse

LOGGER = logging.getLogger(__name__)


class ZurichseeApiClient:
    """API Client for fetching weather data from tecdottir."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the client."""
        self._session = session
        self._base_url = URL(API_BASE_URL)

    async def async_get_measurements(self, station: str) -> MeasurementData | None:
        """Fetch the latest measurement for a specific station."""
        url = self._base_url / "measurements" / station
        params: dict[str, Any] = {
            "limit": 1,
            "sort": "timestamp_cet desc",
        }

        try:
            async with self._session.get(
                url, params=params, timeout=aiohttp.ClientTimeout(total=20)
            ) as response:
                if response.status != 200:
                    raise ZurichseeApiError(
                        f"Failed to fetch data from {station}: {response.status}"
                    )

                data = await response.json()
                parsed = MeasurementResponse.model_validate(data)

                if not parsed.result:
                    return None

                entry = parsed.result[0]
                values = entry.values

                # Flatten the values
                result = MeasurementData()

                # Helper to get value from ValueEntry
                def get_val(key: str) -> Any:
                    if key not in values:
                        return None
                    return values[key].value

                result.air_temperature = get_val("air_temperature")
                result.water_temperature = get_val("water_temperature")
                result.wind_direction = get_val("wind_direction")
                result.wind_force_avg_10min = get_val("wind_force_avg_10min")
                result.wind_gust_max_10min = get_val("wind_gust_max_10min")
                result.wind_speed_avg_10min = get_val("wind_speed_avg_10min")
                result.windchill = get_val("windchill")
                result.barometric_pressure_qfe = get_val("barometric_pressure_qfe")
                result.dew_point = get_val("dew_point")
                result.humidity = get_val("humidity")
                result.precipitation = get_val("precipitation")
                result.global_radiation = get_val("global_radiation")
                result.water_level = get_val("water_level")

                ts_cet = get_val("timestamp_cet")
                if isinstance(ts_cet, str):
                    result.timestamp_cet = datetime.fromisoformat(ts_cet)
                elif isinstance(ts_cet, datetime):
                    result.timestamp_cet = ts_cet

                return result

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
