"""Constants for the Zurichsee Wetterstationen integration."""

from __future__ import annotations

DOMAIN = "zurichsee_ha"
API_BASE_URL = "https://tecdottir.herokuapp.com"

STATIONS = ["mythenquai", "tiefenbrunnen"]
STATION_NAMES = {
    "mythenquai": "Mythenquai",
    "tiefenbrunnen": "Tiefenbrunnen",
}

CONF_UPDATE_INTERVAL = "update_interval"
CONF_STATIONS = "stations"

# Update interval options in seconds
UPDATE_INTERVAL_OPTIONS = {
    900: "15 Minuten",
    1800: "30 Minuten",
    3600: "60 Minuten",
}
DEFAULT_UPDATE_INTERVAL = 1800  # 30 minutes

DEFAULT_OPTIONS = {
    CONF_UPDATE_INTERVAL: DEFAULT_UPDATE_INTERVAL,
    CONF_STATIONS: STATIONS,
}

UPDATE_PLATFORMS: tuple[str, ...] = ("sensor",)
