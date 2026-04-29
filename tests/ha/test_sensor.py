"""Test Zurichsee Wetterstationen sensors."""

import json
from unittest.mock import patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.zurichsee_ha.const import DOMAIN


@pytest.mark.asyncio
async def test_sensors(hass: HomeAssistant) -> None:
    """Test sensor entities are created."""
    with open("tests/fixtures/mythenquai.json") as f:
        mock_data = json.load(f)

    # Mock the API client return value
    with patch(
        "custom_components.zurichsee_ha.api.ZurichseeApiClient.async_get_measurements",
        return_value=None,  # Will be set below
    ) as mock_get:
        # We need to mock the response for both stations if configured
        # But for this test we only use mythenquai
        from custom_components.zurichsee_ha.models import MeasurementValues

        mock_get.return_value = MeasurementValues.model_validate(mock_data["result"][0])

        entry = MockConfigEntry(
            domain=DOMAIN,
            title="Zurichsee",
            options={"stations": ["mythenquai"], "update_interval": 1800},
        )
        entry.add_to_hass(hass)

        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        # Check if sensors exist
        state = hass.states.get("sensor.mythenquai_air_temperature")
        assert state is not None
        assert state.state == "12.5"
        assert state.attributes["unit_of_measurement"] == "°C"

        state = hass.states.get("sensor.mythenquai_water_temperature")
        assert state is not None
        assert state.state == "11.2"
