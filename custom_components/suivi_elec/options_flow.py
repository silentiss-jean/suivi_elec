# -*- coding: utf-8 -*-
"""Options Flow pour Suivi Élec — modification post-installation."""

import voluptuous as vol
import logging
from homeassistant import config_entries
from homeassistant.core import callback

from .const_toremove import (
    DOMAIN,
    ENTITES_POTENTIELLES,
    CONF_MODE, CONF_URL, CONF_TYPE_CONTRAT,
    CONF_PRIX_HT, CONF_PRIX_TTC,
    CONF_PRIX_HT_HP, CONF_PRIX_TTC_HP,
    CONF_PRIX_HT_HC, CONF_PRIX_TTC_HC,
    CONF_HEURE_DEBUT_HP, CONF_HEURE_FIN_HP,
    CONF_ABONNEMENT_ANNUEL
)

from .helpers.api_client import get_energy_entities

_LOGGER = logging.getLogger(__name__)

DEFAULT_MODE = "local"
CONTRATS = ["prix_unique", "heures_pleines_creuses"]

class SuiviElecOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Étape unique pour modifier les options."""
        errors = {}
        current = self.config_entry.options or self.config_entry.data

        # 🔍 Récupération des entités disponibles
        mode = current.get(CONF_MODE, DEFAULT_MODE)
        base_url = current.get(CONF_URL, "local")
        token = current.get(CONF_TOKEN, "")

        entites_detectees = ENTITES_POTENTIELLES
        if mode == "remote":
            try:
                entites_detectees = get_energy_entities(base_url, token) or ENTITES_POTENTIELLES
            except Exception as e:
                _LOGGER.warning("Échec récupération des entités via API : %s", e)
                entites_detectees = ENTITES_POTENTIELLES

        entite_ids = [e["entity_id"] if isinstance(e, dict) else e for e in entites_detectees]

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Optional("entites_actives", default=entite_ids): vol.All([str]),
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
            vol.Optional(CONF_ENTITES_ACTIVES, default=entite_ids): vol.All([str]),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "entites_actives": "Sélectionnez les capteurs à suivre"
            }
        )