# -*- coding: utf-8 -*-
"""Config Flow pour Suivi Élec avec support local/distant, contrat tarifaire et abonnement."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN
from .helpers.api_client import test_api_connection

# 🔑 Clés de configuration
CONF_NAME = "name"
CONF_MODE = "mode"
CONF_TOKEN = "token"
CONF_URL = "base_url"
CONF_TYPE_CONTRAT = "type_contrat"
CONF_PRIX_HT = "prix_ht"
CONF_PRIX_TTC = "prix_ttc"
CONF_PRIX_HT_HP = "prix_ht_hp"
CONF_PRIX_TTC_HP = "prix_ttc_hp"
CONF_PRIX_HT_HC = "prix_ht_hc"
CONF_PRIX_TTC_HC = "prix_ttc_hc"
CONF_HEURE_DEBUT_HP = "heure_debut_hp"
CONF_HEURE_FIN_HP = "heure_fin_hp"
CONF_ABONNEMENT_ANNUEL = "abonnement_annuel"

DEFAULT_NAME = "Suivi Électricité"
DEFAULT_MODE = "local"
CONTRATS = ["prix_unique", "heures_pleines_creuses"]

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Étape 1 : choix du mode et du contrat."""
        if user_input is not None:
            self.config_data = user_input
            return await self.async_step_details()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_MODE, default=DEFAULT_MODE): vol.In(["local", "remote"]),
                vol.Required(CONF_TYPE_CONTRAT, default="prix_unique"): vol.In(CONTRATS),
            }),
            description_placeholders={
                CONF_MODE: "Choisissez local ou distant",
                CONF_TYPE_CONTRAT: "Tarification unique ou HP/HC"
            }
        )

    async def async_step_details(self, user_input=None):
        """Étape 2 : détails selon le mode et le contrat."""
        errors = {}
        mode = self.config_data.get(CONF_MODE)
        type_contrat = self.config_data.get(CONF_TYPE_CONTRAT)

        # 🔧 Construction dynamique du formulaire
        schema_fields = {
            vol.Required(CONF_TOKEN, default=""): str,
            vol.Optional(CONF_ABONNEMENT_ANNUEL, default=0.0): vol.Coerce(float)
        }

        if mode == "remote":
            schema_fields[vol.Required(CONF_URL, default="https://api.edf.fr")] = str

        if type_contrat == "prix_unique":
            schema_fields.update({
                vol.Optional(CONF_PRIX_HT, default=0.0): vol.Coerce(float),
                vol.Optional(CONF_PRIX_TTC, default=0.0): vol.Coerce(float),
            })
        else:
            schema_fields.update({
                vol.Optional(CONF_PRIX_HT_HP, default=0.0): vol.Coerce(float),
                vol.Optional(CONF_PRIX_TTC_HP, default=0.0): vol.Coerce(float),
                vol.Optional(CONF_PRIX_HT_HC, default=0.0): vol.Coerce(float),
                vol.Optional(CONF_PRIX_TTC_HC, default=0.0): vol.Coerce(float),
                vol.Optional(CONF_HEURE_DEBUT_HP, default="06:00"): str,
                vol.Optional(CONF_HEURE_FIN_HP, default="22:00"): str,
            })

        if user_input is not None:
            token = user_input.get(CONF_TOKEN)
            base_url = user_input.get(CONF_URL, "local")

            # 🔐 Validation API si mode distant
            try:
                if mode == "remote" and not test_api_connection(base_url, token):
                    errors[CONF_TOKEN] = "token_invalide"
            except Exception:
                errors[CONF_TOKEN] = "erreur_connexion"

            if not errors:
                data = {**self.config_data, **user_input}
                return self.async_create_entry(title=data.get(CONF_NAME, DEFAULT_NAME), data=data)

        return self.async_show_form(
            step_id="details",
            data_schema=vol.Schema(schema_fields),
            errors=errors,
            description_placeholders={
                CONF_TOKEN: "Jeton requis pour accéder à l'API",
                CONF_URL: "URL de l'instance distante",
                CONF_PRIX_HT: "Prix HT du kWh",
                CONF_PRIX_TTC: "Prix TTC du kWh",
                CONF_PRIX_HT_HP: "Prix HT Heure Pleine",
                CONF_PRIX_TTC_HP: "Prix TTC Heure Pleine",
                CONF_PRIX_HT_HC: "Prix HT Heure Creuse",
                CONF_PRIX_TTC_HC: "Prix TTC Heure Creuse",
                CONF_HEURE_DEBUT_HP: "Début HP (ex: 06:00)",
                CONF_HEURE_FIN_HP: "Fin HP (ex: 22:00)",
                CONF_ABONNEMENT_ANNUEL: "Montant annuel de l'abonnement"
            }
        )

#    @staticmethod
#    @callback
#    def async_get_options_flow(config_entry):
#        from .options_flow import SuiviElecOptionsFlow
#        return SuiviElecOptionsFlow(config_entry)