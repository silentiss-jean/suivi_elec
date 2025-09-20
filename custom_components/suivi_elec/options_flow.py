# -*- coding: utf-8 -*-
"""Formulaire de configuration pour Suivi Élec."""

import voluptuous as vol
from homeassistant import config_entries

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry
        self.type_contrat = "prix_unique"

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            self.type_contrat = user_input["type_contrat"]
            return await self.async_step_tarifs()

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("type_contrat", default="prix_unique"): vol.In([
                    "prix_unique",
                    "Heures_Pleine_Heures_Creuses"
                ])
            }),
            description_placeholders={
                "prix_unique": "Tarif simple, un seul prix du kWh",
                "Heures_Pleine_Heures_Creuses": "Tarif différencié selon les heures"
            }
        )

    async def async_step_tarifs(self, user_input=None):
        if self.type_contrat == "prix_unique":
            schema = vol.Schema({
                vol.Required("abonnement_ht", default=10.0): vol.Coerce(float),
                vol.Optional("abonnement_ttc"): vol.Coerce(float),
                vol.Required("prix_kwh_ht", default=0.15): vol.Coerce(float),
                vol.Optional("prix_kwh_ttc"): vol.Coerce(float)
            })
        else:
            schema = vol.Schema({
                vol.Required("abonnement_ht", default=10.0): vol.Coerce(float),
                vol.Optional("abonnement_ttc"): vol.Coerce(float),
                vol.Required("prix_hp_ht", default=0.18): vol.Coerce(float),
                vol.Optional("prix_hp_ttc"): vol.Coerce(float),
                vol.Required("prix_hc_ht", default=0.12): vol.Coerce(float),
                vol.Optional("prix_hc_ttc"): vol.Coerce(float)
            })

        if user_input is not None:
            return self.async_create_entry(title="Tarifs Suivi Élec", data=user_input)

        return self.async_show_form(
            step_id="tarifs",
            data_schema=schema,
            description_placeholders={
                "abonnement_ttc": "Facultatif — peut varier selon les taxes appliquées",
                "prix_kwh_ttc": "Facultatif — peut varier selon les taxes appliquées",
                "prix_hp_ttc": "Facultatif — peut varier selon les taxes appliquées",
                "prix_hc_ttc": "Facultatif — peut varier selon les taxes appliquées"
            }
        )
