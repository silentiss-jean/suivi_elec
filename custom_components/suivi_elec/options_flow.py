from homeassistant import config_entries
import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)

class SuiviElecOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        try:
            current = self.config_entry.options or self.config_entry.data

            data_schema = vol.Schema({
                vol.Required("mode", default=current.get("mode", "local")): vol.In(["local", "remote"]),
                vol.Required("type_contrat", default=current.get("type_contrat", "prix_unique")): vol.In(["prix_unique", "heures_pleines_creuses"]),
                vol.Optional("prix_ht", default=current.get("prix_ht", 0.0)): vol.Coerce(float),
                vol.Optional("prix_ttc", default=current.get("prix_ttc", 0.0)): vol.Coerce(float),
            })

            if user_input is not None:
                return self.async_create_entry(title="Options", data=user_input)

            return self.async_show_form(
                step_id="init",
                data_schema=data_schema,
                errors={}
            )
        except Exception as e:
            _LOGGER.error("Erreur dans async_step_init : %s", e)
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({}),
                errors={"base": "erreur_interne"}
            )