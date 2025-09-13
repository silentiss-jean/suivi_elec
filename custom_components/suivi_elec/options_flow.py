# -*- coding: utf-8 -*-
"""Options Flow pour Suivi Élec — modification post-installation."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_MODE, CONF_URL, CONF_TYPE_CONTRAT,
    CONF_PRIX_HT, CONF_PRIX_TTC,
    CONF_PRIX_HT_HP, CONF_PRIX_TTC_HP,
    CONF_PRIX_HT_HC, CONF_PRIX_TTC_HC,
    CONF_HEURE_DEBUT_HP, CONF_HEURE_FIN_HP,
    CONF_ABONNEMENT_ANNUEL
)

DEFAULT_MODE = "local"
CONTRATS = ["prix_unique", "heures_pleines_creuses"]

class SuiviElecOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        current = self.config_entry.options or self.config_entry.data

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_MODE, default=current.get(CONF_MODE, DEFAULT_MODE)): vol.In(["local", "remote"]),
            vol.Optional(CONF_URL, default=current.get(CONF_URL, "")): str,
            vol.Required(CONF_TYPE_CONTRAT, default=current.get(CONF_TYPE_CONTRAT, "prix_unique")): vol.In(CONTRATS),
            vol.Optional(CONF_PRIX_HT, default=current.get(CONF_PRIX_HT, 0.0)): vol.Coerce(float),
            vol.Optional(CONF_PRIX_TTC, default=current.get(CONF_PRIX_TTC, 0.0)): vol.Coerce(float),
            vol.Optional(CONF_PRIX_HT_HP, default=current.get(CONF_PRIX_HT_HP, 0.0)): vol.Coerce(float),
            vol.Optional(CONF_PRIX_TTC_HP, default=current.get(CONF_PRIX_TTC_HP, 0.0)): vol.Coerce(float),
            vol.Optional(CONF_PRIX_HT_HC, default=current.get(CONF_PRIX_HT_HC, 0.0)): vol.Coerce(float),
            vol.Optional(CONF_PRIX_TTC_HC, default=current.get(CONF_PRIX_TTC_HC, 0.0)): vol.Coerce(float),
            vol.Optional(CONF_HEURE_DEBUT_HP, default=current.get(CONF_HEURE_DEBUT_HP, "06:00")): str,
            vol.Optional(CONF_HEURE_FIN_HP, default=current.get(CONF_HEURE_FIN_HP, "22:00")): str,
            vol.Optional(CONF_ABONNEMENT_ANNUEL, default=current.get(CONF_ABONNEMENT_ANNUEL, 0.0)): vol.Coerce(float),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors
        )
