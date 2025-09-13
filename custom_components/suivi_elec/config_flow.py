from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_API_TOKEN, CONF_BASE_URL

_LOGGER = logging.getLogger(__name__)

class SuiviElecConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gérer le flux de configuration pour Suivi Élec."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Première étape de configuration."""
        errors = {}

        if user_input is not None:
            # Validation des tarifs
            try:
                kwh = float(user_input["kwh"])
                hp = float(user_input["hp"])
                hc = float(user_input["hc"])
            except ValueError:
                errors["base"] = "invalid_tarif"

            # Test API token avant d'accepter
            if not errors:
                valid = await self._test_api_token(user_input[CONF_API_TOKEN], user_input[CONF_BASE_URL])
                if valid:
                    return self.async_create_entry(title="Suivi Élec", data=user_input)
                else:
                    errors["base"] = "invalid_token"

        # Formulaire de configuration
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_TOKEN): str,
                vol.Required(CONF_BASE_URL, default="https://api.edf.fr"): str,
                vol.Required("kwh", default=0.15): float,
                vol.Required("hp", default=0.18): float,
                vol.Required("hc", default=0.12): float,
            }),
            errors=errors,
        )

    async def _test_api_token(self, api_token: str, base_url: str) -> bool:
        """Tester la validité du jeton API."""
        from .helpers.api_client import test_api_token
        return await test_api_token(api_token, base_url)