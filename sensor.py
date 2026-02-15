"""Platform for Nuki Web API sensor integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Nuki sensors from a config entry."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    
    # Create battery sensor for each smartlock
    entities = []
    for smartlock in coordinator.data:
        entities.append(NukiBatterySensor(coordinator, smartlock))
    
    async_add_entities(entities)


class NukiBatterySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Nuki Smart Lock battery sensor."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, smartlock_data: dict[str, Any]) -> None:
        """Initialize the battery sensor."""
        super().__init__(coordinator)
        self._smartlock_id = smartlock_data["smartlockId"]
        lock_name = smartlock_data.get("name", f"Nuki Lock {self._smartlock_id}")
        
        self._attr_name = f"{lock_name} Battery"
        self._attr_unique_id = f"nuki_{self._smartlock_id}_battery"
        
        # Associate with the same device as the lock
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._smartlock_id)},
        }
        
        # Update initial state
        self._update_from_data(smartlock_data)

    def _update_from_data(self, smartlock_data: dict[str, Any]) -> None:
        """Update the sensor state from smartlock data."""
        state = smartlock_data.get("state", {})
        
        # Battery critical is a boolean, but we might have batteryChargeState (percentage)
        # Different Nuki models report differently:
        # - batteryChargeState: 0-100 (percentage) - newer models
        # - batteryCritical: boolean - all models
        # - batteryCharging: boolean - models with rechargeable battery
        
        battery_charge = state.get("batteryChargeState")
        battery_critical = state.get("batteryCritical", False)
        
        if battery_charge is not None:
            # We have percentage
            self._attr_native_value = battery_charge
        elif battery_critical:
            # Only have critical flag - estimate based on that
            # Critical is typically < 20%
            self._attr_native_value = 15  # Estimate low battery
        else:
            # Battery is not critical, estimate good level
            self._attr_native_value = 80  # Estimate healthy battery
        
        # Store charging state as attribute
        self._battery_charging = state.get("batteryCharging", False)
        self._battery_critical = battery_critical

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "battery_critical": self._battery_critical,
            "battery_charging": self._battery_charging,
        }

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Find the updated data for this specific smartlock
        for smartlock in self.coordinator.data:
            if smartlock["smartlockId"] == self._smartlock_id:
                self._update_from_data(smartlock)
                break
        
        self.async_write_ha_state()
