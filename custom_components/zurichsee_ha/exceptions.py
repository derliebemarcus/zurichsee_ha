"""Exceptions for the Zurichsee Wetterstationen integration."""

from homeassistant.exceptions import HomeAssistantError


class ZurichseeApiError(HomeAssistantError):
    """Error to indicate a general API error."""
