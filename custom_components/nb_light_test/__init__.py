"""The light_log_test integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    ATTR_COLOR,
    ATTR_ENTITY_ID,
    ATTR_NAME,
    DEFAULT_COLOR,
    DEFAULT_NAME,
    DOMAIN,
)

logger = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up light_log_test from a config entry."""

    # Define test service action
    async def on_and_log(call):
        """Handle the Service Call"""  # noqa: D400, D415
        name = call.data.get(ATTR_NAME, DEFAULT_NAME)
        color = call.data.get(ATTR_COLOR, DEFAULT_COLOR)
        target = ATTR_ENTITY_ID
        state = hass.states.get(target)

        # Construct data block
        data = {
            "entity_id": target,
            "rgb_color": color,
        }

        # Run service call
        if state == "off":
            off_message = "Light found to be off, " + name
            logger.info(off_message)
            hass.services.call("light", "turn_on", data, False)
        else:
            on_message = "Light on, " + name + ", No action taken."
            logger.info(on_message)

    await hass.services.async_register(DOMAIN, "on_and_log", on_and_log)

    await hass.config_entries.async_forward_entry_setups(entry, (Platform.SENSOR,))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, (Platform.SENSOR,))
