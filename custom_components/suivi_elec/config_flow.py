from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class SuiviElecConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self.mode = user_input["mode"]
            return await self.async_step_details()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("mode", default="local"): vol.In(["local", "cloud"])
            }),
            description_placeholders={
                "local": "Instance Home Assistant locale",
                "cloud": "Instance distante via API"
            }
        )

    async def async_step_details(self, user_input=None):
        if self.mode == "local":
            schema = vol.Schema({
                vol.Required("base_url", default="http://homeassistant.local:8123"): str,
                vol.Optional("nom_utilisateur", default="admin"): str
            })
        else:
            schema = vol.Schema({
                vol.Required("base_url", default="https://api.edf.fr"): str,
                vol.Required("api_token"): str
            })

        if user_input is not None:
            return self.async_create_entry(title="Suivi Élec", data={**user_input, "mode": self.mode})

        return self.async_show_form(step_id="details", data_schema=schema)
