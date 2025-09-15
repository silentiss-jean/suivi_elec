from homeassistant import config_entries
import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("✅ Import de options_flow.py réussi")

class SuiviElecOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry
        _LOGGER.debug("✅ SuiviElecOptionsFlow initialisé avec config_entry: %s", config_entry)

    async def async_step_init(self, user_input=None):
        _LOGGER.debug("✅ async_step_init appelé avec user_input: %s", user_input)
        return self.async_create_entry(title="Options", data={})