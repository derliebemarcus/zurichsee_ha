"""Test Zurichsee Wetterstationen config flow."""

from unittest.mock import patch

import pytest
from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.zurichsee_ha.const import DOMAIN


@pytest.mark.asyncio
async def test_user_flow(hass: HomeAssistant) -> None:
    """Test the user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch(
        "custom_components.zurichsee_ha.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"stations": ["mythenquai"], "update_interval": 1800},
        )
        await hass.async_block_till_done()

    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["title"] == "Zürichsee Wetterstationen"
    assert result["options"] == {"stations": ["mythenquai"], "update_interval": 1800}
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.asyncio
async def test_single_instance(hass: HomeAssistant) -> None:
    """Test that only one instance is allowed."""
    # Setup first entry
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Zurichsee",
        data={},
        options={},
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
