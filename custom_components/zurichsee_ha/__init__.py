"""Zurichsee Wetterstationen integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ZurichseeApiClient
from .const import CONF_STATIONS, CONF_UPDATE_INTERVAL, DEFAULT_OPTIONS
from .coordinator import ZurichseeCoordinator

LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Zurichsee Wetterstationen from a config entry."""
    session = async_get_clientsession(hass)
    api = ZurichseeApiClient(session)

    stations = entry.options.get(CONF_STATIONS, DEFAULT_OPTIONS[CONF_STATIONS])
    update_interval = entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_OPTIONS[CONF_UPDATE_INTERVAL])

    coordinator = ZurichseeCoordinator(
        hass,
        api,
        stations=stations,
        update_interval=update_interval,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Clean up runtime data if needed
        pass

    return unload_ok  # type: ignore[no-any-return]


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
