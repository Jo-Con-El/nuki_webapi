"""Platform for Nuki Web API lock integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NUKI_STATES_MAP

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Nuki locks from a config entry."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    client = data["client"]
    
    # Create entities for each smartlock found
    entities = []
    for smartlock in coordinator.data:
        entities.append(NukiLock(coordinator, client, smartlock))
    
    async_add_entities(entities)


class NukiLock(CoordinatorEntity, LockEntity):
    """Representation of a Nuki Smart Lock."""

    def __init__(self, coordinator, client, smartlock_data: dict[str, Any]) -> None:
        """Initialize the lock."""
        super().__init__(coordinator)
        self._client = client
        self._smartlock_id = smartlock_data["smartlockId"]
        self._attr_name = smartlock_data.get("name", f"Nuki Lock {self._smartlock_id}")
        self._attr_unique_id = f"nuki_{self._smartlock_id}"
        
        # Device information
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._smartlock_id)},
            "name": self._attr_name,
            "manufacturer": "Nuki",
            "model": "Smart Lock",
        }
        
        # Update initial state
        self._update_from_data(smartlock_data)

    def _update_from_data(self, smartlock_data: dict[str, Any]) -> None:
        """Update the lock state from smartlock data."""
        state = smartlock_data.get("state", {})
        self._state = state.get("state", 255)  # 255 = undefined
        self._battery_critical = state.get("batteryCritical", False)
        
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    @property
    def is_locked(self) -> bool | None:
        """Return true if the lock is locked."""
        state_str = NUKI_STATES_MAP.get(self._state, "unknown")
        if state_str == "locked":
            return True
        elif state_str in ["unlocked", "unlatched"]:
            return False
        return None

    @property
    def is_locking(self) -> bool:
        """Return true if the lock is locking."""
        return NUKI_STATES_MAP.get(self._state) == "locking"

    @property
    def is_unlocking(self) -> bool:
        """Return true if the lock is unlocking."""
        return NUKI_STATES_MAP.get(self._state) == "unlocking"

    @property
    def is_jammed(self) -> bool:
        """Return true if the lock is jammed."""
        return NUKI_STATES_MAP.get(self._state) == "jammed"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "battery_critical": self._battery_critical,
            "nuki_state": self._state,
            "nuki_state_name": NUKI_STATES_MAP.get(self._state, "unknown"),
        }

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the device."""
        _LOGGER.debug("Locking Nuki lock %s", self._smartlock_id)
        await self._client.lock(self._smartlock_id)
        # Immediate refresh
        await self.coordinator.async_request_refresh()
        # Schedule a delayed refresh in the background (non-blocking)
        # Nuki lock takes 1-3 seconds to complete the action
        self._schedule_delayed_refresh()

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the device."""
        _LOGGER.debug("Unlocking Nuki lock %s", self._smartlock_id)
        await self._client.unlock(self._smartlock_id)
        # Immediate refresh
        await self.coordinator.async_request_refresh()
        # Schedule a delayed refresh in the background
        self._schedule_delayed_refresh()

    async def async_open(self, **kwargs: Any) -> None:
        """Open the door latch."""
        _LOGGER.debug("Unlatching Nuki lock %s", self._smartlock_id)
        await self._client.unlatch(self._smartlock_id)
        # Immediate refresh
        await self.coordinator.async_request_refresh()
        # Schedule a delayed refresh in the background
        self._schedule_delayed_refresh()

    def _schedule_delayed_refresh(self) -> None:
        """Schedule a delayed refresh to catch the final lock state."""
        async def delayed_refresh():
            """Wait and then refresh."""
            await asyncio.sleep(3)
            await self.coordinator.async_request_refresh()

        # Create task in the background (non-blocking)
        asyncio.create_task(delayed_refresh())

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Find the updated data for this specific smartlock
        for smartlock in self.coordinator.data:
            if smartlock["smartlockId"] == self._smartlock_id:
                self._update_from_data(smartlock)
                break
        
        self.async_write_ha_state()
