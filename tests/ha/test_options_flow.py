"""Test Zurichsee Wetterstationen options flow."""

from unittest.mock import patch

import pytest
from homeassistant import data_entry_flow
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.zurichsee_ha.const import DOMAIN


@pytest.mark.asyncio
async def test_options_flow(hass: HomeAssistant) -> None:
    """Test the options flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Zurichsee",
        data={},
        options={"stations": ["mythenquai"], "update_interval": 1800},
    )
    entry.add_to_hass(hass)

    # Initialize the options flow
    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "init"

    # Configure the options
    with patch(
        "custom_components.zurichsee_ha.async_setup_entry",
        return_value=True,
    ):
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={"stations": ["mythenquai", "tiefenbrunnen"], "update_interval": "3600"},
        )
        await hass.async_block_till_done()

    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["data"] == {"stations": ["mythenquai", "tiefenbrunnen"], "update_interval": 3600}

    # Verify that async_reload_entry is called (coverage for __init__.py:58)
    from custom_components.zurichsee_ha import async_reload_entry

    with patch("homeassistant.config_entries.ConfigEntries.async_reload") as mock_reload:
        await async_reload_entry(hass, entry)
        mock_reload.assert_called_once_with(entry.entry_id)
