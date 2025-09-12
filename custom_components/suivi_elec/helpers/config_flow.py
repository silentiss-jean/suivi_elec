from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_API_TOKEN, CONF_BASE_URL
from .helpers.api_client import test_api_token

_LOGGER = logging.getLogger(__name__)

class SuiviElecConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Suivi Élec."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        errors = {}

        if user_input is not None:
            # Test API token before accepting
            valid = await test_api_token(user_input[CONF_API_TOKEN], user_input[CONF_BASE_URL])
            if valid:
                return self.async_create_entry(title="Suivi Élec", data=user_input)
            else:
                errors["base"] = "invalid_token"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_TOKEN): str,
                vol.Required(CONF_BASE_URL, default="https://api.edf.fr"): str,
            }),
            errors=errors,
        )