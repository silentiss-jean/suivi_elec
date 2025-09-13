# -*- coding: utf-8 -*-
"""Config Flow complet pour Suivi Élec avec support HP/HC, abonnement et prix unique."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

DOMAIN = "suivi_elec"

# 🔑 Clés de configuration
CONF_NAME = "name"
CONF_MODE = "mode"
CONF_TOKEN = "token"
CONF_URL = "url"
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

# 🧰 Valeurs par défaut
DEFAULT_NAME = "Suivi Électricité"
DEFAULT_MODE = "local"
CONTRATS = ["prix_unique", "heures_pleines_creuses"]

class SuiviElecConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            name = user_input.get(CONF_NAME, DEFAULT_NAME)
            mode = user_input.get(CONF_MODE, DEFAULT_MODE)
            token = user_input.get(CONF_TOKEN, "")
            url = user_input.get(CONF_URL, "")
            type_contrat = user_input.get(CONF_TYPE_CONTRAT, "prix_unique")
            abonnement_annuel = user_input.get(CONF_ABONNEMENT_ANNUEL, 0.0)

            # 🔐 Validation du token
            if not token or len(token) < 100:
                errors[CONF_TOKEN] = "token_invalide"

            # 🌐 Validation de l'URL en mode distant
            if mode == "remote" and not url:
                errors[CONF_URL] = "url_requise"

            # 💶 Tarification selon le contrat
            if type_contrat == "prix_unique":
                prix_ht = user_input.get(CONF_PRIX_HT, 0.0)
                prix_ttc = user_input.get(CONF_PRIX_TTC, prix_ht * 1.2)
            else:
                prix_ht_hp = user_input.get(CONF_PRIX_HT_HP, 0.0)
                prix_ttc_hp = user_input.get(CONF_PRIX_TTC_HP, prix_ht_hp * 1.2)
                prix_ht_hc = user_input.get(CONF_PRIX_HT_HC, 0.0)
                prix_ttc_hc = user_input.get(CONF_PRIX_TTC_HC, prix_ht_hc * 1.2)
                heure_debut_hp = user_input.get(CONF_HEURE_DEBUT_HP, "06:00")
                heure_fin_hp = user_input.get(CONF_HEURE_FIN_HP, "22:00")

            if not errors:
                data = {
                    CONF_NAME: name,
                    CONF_MODE: mode,
                    CONF_TOKEN: token,
                    CONF_URL: url,
                    CONF_TYPE_CONTRAT: type_contrat,
                    CONF_ABONNEMENT_ANNUEL: abonnement_annuel,
                }
                if type_contrat == "prix_unique":
                    data.update({
                        CONF_PRIX_HT: prix_ht,
                        CONF_PRIX_TTC: prix_ttc
                    })
                else:
                    data.update({
                        CONF_PRIX_HT_HP: prix_ht_hp,
                        CONF_PRIX_TTC_HP: prix_ttc_hp,
                        CONF_PRIX_HT_HC: prix_ht_hc,
                        CONF_PRIX_TTC_HC: prix_ttc_hc,
                        CONF_HEURE_DEBUT_HP: heure_debut_hp,
                        CONF_HEURE_FIN_HP: heure_fin_hp
                    })
                return self.async_create_entry(title=name, data=data)

        # 🧾 Formulaire utilisateur
        data_schema = vol.Schema({
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Required(CONF_MODE, default=DEFAULT_MODE): vol.In(["local", "remote"]),
            vol.Required(CONF_TOKEN, default=""): str,
            vol.Optional(CONF_URL, default=""): str,
            vol.Required(CONF_TYPE_CONTRAT, default="prix_unique"): vol.In(CONTRATS),
            vol.Optional(CONF_PRIX_HT, default=0.0): vol.Coerce(float),
            vol.Optional(CONF_PRIX_TTC, default=0.0): vol.Coerce(float),
            vol.Optional(CONF_PRIX_HT_HP, default=0.0): vol.Coerce(float),
            vol.Optional(CONF_PRIX_TTC_HP, default=0.0): vol.Coerce(float),
            vol.Optional(CONF_PRIX_HT_HC, default=0.0): vol.Coerce(float),
            vol.Optional(CONF_PRIX_TTC_HC, default=0.0): vol.Coerce(float),
            vol.Optional(CONF_HEURE_DEBUT_HP, default="06:00"): str,
            vol.Optional(CONF_HEURE_FIN_HP, default="22:00"): str,
            vol.Optional(CONF_ABONNEMENT_ANNUEL, default=0.0): vol.Coerce(float),
        })

        description_placeholders = {
            CONF_PRIX_HT: "Prix HT (si vide → 0)",
            CONF_PRIX_TTC: "Prix TTC (si vide → 0)",
            CONF_PRIX_HT_HP: "Prix HT Heure Pleine",
            CONF_PRIX_TTC_HP: "Prix TTC Heure Pleine",
            CONF_PRIX_HT_HC: "Prix HT Heure Creuse",
            CONF_PRIX_TTC_HC: "Prix TTC Heure Creuse",
            CONF_HEURE_DEBUT_HP: "Heure de début HP",
            CONF_HEURE_FIN_HP: "Heure de fin HP",
            CONF_ABONNEMENT_ANNUEL: "Abonnement annuel",
            CONF_URL: "Requis uniquement en mode remote",
            CONF_TOKEN: "Token d'accès requis"
        }

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders=description_placeholders
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        from .options_flow import SuiviElecOptionsFlow
        return SuiviElecOptionsFlow(config_entry)