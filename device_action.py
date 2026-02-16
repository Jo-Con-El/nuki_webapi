"""Provides device actions for Nuki Web API."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.components.lock import DOMAIN as LOCK_DOMAIN
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_TYPE,
)
from homeassistant.core import Context, HomeAssistant
from homeassistant.helpers import entity_registry as er
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

# Define action types
ACTION_TYPE_LOCK = "lock"
ACTION_TYPE_UNLOCK = "unlock"
ACTION_TYPE_OPEN = "open"
ACTION_TYPE_LOCK_N_GO = "lock_n_go"

ACTION_TYPES = {
    ACTION_TYPE_LOCK,
    ACTION_TYPE_UNLOCK,
    ACTION_TYPE_OPEN,
    ACTION_TYPE_LOCK_N_GO,
}

# Schema for lock_n_go action
ACTION_SCHEMA = cv.DEVICE_ACTION_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(ACTION_TYPES),
        vol.Required(CONF_ENTITY_ID): cv.entity_id_or_uuid,
        vol.Optional("unlatch", default=False): bool,
    }
)


async def async_get_actions(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device actions for Nuki locks."""
    registry = er.async_get(hass)
    actions = []

    # Get all entities for this device
    for entry in er.async_entries_for_device(registry, device_id):
        if entry.domain != LOCK_DOMAIN:
            continue

        base_action = {
            CONF_DEVICE_ID: device_id,
            CONF_DOMAIN: DOMAIN,
            CONF_ENTITY_ID: entry.id,
        }

        actions.append({**base_action, CONF_TYPE: ACTION_TYPE_LOCK})
        actions.append({**base_action, CONF_TYPE: ACTION_TYPE_UNLOCK})
        actions.append({**base_action, CONF_TYPE: ACTION_TYPE_OPEN})
        actions.append({**base_action, CONF_TYPE: ACTION_TYPE_LOCK_N_GO})

    return actions


async def async_call_action_from_config(
    hass: HomeAssistant, config: dict, variables: dict, context: Context | None
) -> None:
    """Execute a device action."""
    action_type = config[CONF_TYPE]
    entity_id = config[CONF_ENTITY_ID]

    service_data = {ATTR_ENTITY_ID: entity_id}

    if action_type == ACTION_TYPE_LOCK:
        await hass.services.async_call(
            LOCK_DOMAIN, "lock", service_data, blocking=True, context=context
        )
    elif action_type == ACTION_TYPE_UNLOCK:
        await hass.services.async_call(
            LOCK_DOMAIN, "unlock", service_data, blocking=True, context=context
        )
    elif action_type == ACTION_TYPE_OPEN:
        await hass.services.async_call(
            LOCK_DOMAIN, "open", service_data, blocking=True, context=context
        )
    elif action_type == ACTION_TYPE_LOCK_N_GO:
        unlatch = config.get("unlatch", False)
        service_data["unlatch"] = unlatch
        await hass.services.async_call(
            DOMAIN, "lock_n_go", service_data, blocking=True, context=context
        )


async def async_get_action_capabilities(
    hass: HomeAssistant, config: dict
) -> dict[str, vol.Schema]:
    """List action capabilities."""
    action_type = config[CONF_TYPE]

    if action_type == ACTION_TYPE_LOCK_N_GO:
        return {
            "extra_fields": vol.Schema(
                {
                    vol.Optional("unlatch", default=False): bool,
                }
            )
        }

    return {}
