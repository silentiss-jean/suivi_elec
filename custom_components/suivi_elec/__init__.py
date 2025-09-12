from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, ENTITES_POTENTIELLES

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    mode = entry.data.get("mode", "local")
    base_url = entry.data.get("base_url")
    entites_actives = entry.options.get("entites_actives", ENTITES_POTENTIELLES)

    for entity_id in entites_actives:
        base_attrs = {
            "unit_of_measurement": "€",
            "friendly_name": f"[{mode.capitalize()}] {entity_id.split('.')[-1].replace('_', ' ').capitalize()}",
            "source": base_url,
            "integration": "suivi_elec"
        }

        hass.states.async_set(entity_id, "0", base_attrs)

    return True
