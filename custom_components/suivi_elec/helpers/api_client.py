# -*- coding: utf-8 -*-
"""Options Flow pour Suivi Élec : permet de modifier les entités actives et les tarifs."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, ENTITES_POTENTIELLES
from .api_client import get_energy_entities

class SuiviElecOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Étape unique pour modifier les options."""
        errors = {}

        # 🔍 Récupération des entités disponibles
        mode = self.config_entry.data.get("mode", "local")
        base_url = self.config_entry.data.get("base_url", "local")
        token = self.config_entry.data.get("token", "")

        entites_detectees = ENTITES_POTENTIELLES
        if mode == "remote":
            entites_detectees = get_energy_entities(base_url, token) or ENTITES_POTENTIELLES

        entite_ids = [e["entity_id"] if isinstance(e, dict) else e for e in entites_detectees]

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Optional("entites_actives", default=entite_ids): vol.All([str])
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "entites_actives": "Sélectionnez les capteurs à suivre"
            }
        )