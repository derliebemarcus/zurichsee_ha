"""Test Zurichsee Wetterstationen coordinator."""

from unittest.mock import MagicMock

import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.zurichsee_ha.coordinator import ZurichseeCoordinator
from custom_components.zurichsee_ha.exceptions import ZurichseeApiError


@pytest.mark.asyncio
async def test_coordinator_update_error(hass: MagicMock) -> None:
    """Test coordinator update failure."""
    api = MagicMock()
    api.async_get_measurements.side_effect = ZurichseeApiError("API Error")
    
    coordinator = ZurichseeCoordinator(
        hass=hass,
        api=api,
        stations=["mythenquai"],
        update_interval=1800,
    )
    
    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()
