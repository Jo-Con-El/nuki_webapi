"""Config flow for Nuki Web API integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .api import NukiWebApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("api_token"): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    client = NukiWebApiClient(data["api_token"])
    
    try:
        # Try to get smartlocks to validate the token
        smartlocks = await client.get_smartlocks()
        
        if not smartlocks:
            raise NoSmartlocksFound
        
        return {"title": f"Nuki Web API ({len(smartlocks)} devices)"}
    
    except Exception as err:
        _LOGGER.error("Error validating API token: %s", err)
        raise InvalidAuth from err


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nuki Web API."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except NoSmartlocksFound:
                errors["base"] = "no_smartlocks"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Create the config entry
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


class NoSmartlocksFound(HomeAssistantError):
    """Error to indicate no smartlocks were found."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
