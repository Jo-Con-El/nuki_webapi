"""The Nuki Web API integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import NukiWebApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.LOCK]
SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Nuki Web API from a config entry."""
    api_token = entry.data["api_token"]
    
    # Create API client
    client = NukiWebApiClient(api_token)
    
    # Create data update coordinator
    async def async_update_data():
        """Fetch data from API endpoint."""
        try:
            smartlocks = await client.get_smartlocks()
            return smartlocks
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
    
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Nuki Web API",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()
    
    # Store client and coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
