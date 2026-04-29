"""Config flow for Zurichsee Wetterstationen integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_STATIONS,
    CONF_UPDATE_INTERVAL,
    DEFAULT_OPTIONS,
    DOMAIN,
    STATION_NAMES,
    UPDATE_INTERVAL_OPTIONS,
)


class ZurichseeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zurichsee Wetterstationen."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="Zürichsee Wetterstationen",
                data={},
                options={
                    CONF_STATIONS: user_input[CONF_STATIONS],
                    CONF_UPDATE_INTERVAL: int(user_input[CONF_UPDATE_INTERVAL]),
                },
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_STATIONS, default=DEFAULT_OPTIONS[CONF_STATIONS]): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            SelectOptionDict(value=k, label=v) for k, v in STATION_NAMES.items()
                        ],
                        mode=SelectSelectorMode.DROPDOWN,
                        multiple=True,
                    )
                ),
                vol.Required(
                    CONF_UPDATE_INTERVAL, default=DEFAULT_OPTIONS[CONF_UPDATE_INTERVAL]
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            SelectOptionDict(value=str(k), label=v)
                            for k, v in UPDATE_INTERVAL_OPTIONS.items()
                        ],
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> ZurichseeOptionsFlowHandler:
        """Get the options flow for this handler."""
        return ZurichseeOptionsFlowHandler(config_entry)


class ZurichseeOptionsFlowHandler(OptionsFlow):
    """Handle options flow for Zurichsee Wetterstationen."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            user_input[CONF_UPDATE_INTERVAL] = int(user_input[CONF_UPDATE_INTERVAL])
            return self.async_create_entry(title="", data=user_input)

        options = self._config_entry.options
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_STATIONS,
                    default=options.get(CONF_STATIONS, DEFAULT_OPTIONS[CONF_STATIONS]),
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            SelectOptionDict(value=k, label=v) for k, v in STATION_NAMES.items()
                        ],
                        mode=SelectSelectorMode.DROPDOWN,
                        multiple=True,
                    )
                ),
                vol.Required(
                    CONF_UPDATE_INTERVAL,
                    default=options.get(
                        CONF_UPDATE_INTERVAL, DEFAULT_OPTIONS[CONF_UPDATE_INTERVAL]
                    ),
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            SelectOptionDict(value=str(k), label=v)
                            for k, v in UPDATE_INTERVAL_OPTIONS.items()
                        ],
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)
