import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

DOMAIN = "suivi_elec"

class SuiviElecConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Sauvegarde des données dans entry.data
            return self.async_create_entry(title="Suivi Élec", data=user_input)

        # Schéma du formulaire
        data_schema = vol.Schema({
            vol.Required("base_url", default="http://homeassistant.local:8123"): str,
            vol.Required("ha_token"): str,
            vol.Optional("is_local", default=True): bool
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SuiviElecOptionsFlow(config_entry)


class SuiviElecOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional("auto_add_entities", default=True): bool,
            vol.Optional("enable_polling", default=True): bool
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)
