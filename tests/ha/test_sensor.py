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
    ) as mock_get:
        from datetime import datetime

        from custom_components.zurichsee_ha.models import MeasurementData

        # Create a mock data object that matches what the client returns
        vals = mock_data["result"][0]["values"]
        mock_get.return_value = MeasurementData(
            air_temperature=vals["air_temperature"]["value"],
            water_temperature=vals["water_temperature"]["value"],
            timestamp_cet=datetime.fromisoformat(vals["timestamp_cet"]["value"]),
        )

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

@pytest.mark.asyncio
async def test_sensor_missing_data(hass: HomeAssistant) -> None:
    """Test sensor behavior when data is missing."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Zurichsee",
        options={"stations": ["mythenquai"], "update_interval": 1800},
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.zurichsee_ha.api.ZurichseeApiClient.async_get_measurements",
        return_value=None,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        state = hass.states.get("sensor.mythenquai_air_temperature")
        # The sensor is created but its state should be unknown/none
        assert state is not None
        assert state.state == "unknown"
