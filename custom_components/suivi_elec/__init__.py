from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, ENTITES_POTENTIELLES

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurer l'intégration Suivi Élec à partir d'une entrée de configuration."""
    mode = entry.data.get("mode", "local")
    base_url = entry.data.get("base_url")
    entites_actives = entry.options.get("entites_actives", ENTITES_POTENTIELLES)

    # Récupérer les tarifs configurés
    tarifs = {
        "kwh": entry.data.get("kwh", 0.15),
        "hp": entry.data.get("hp", 0.18),
        "hc": entry.data.get("hc", 0.12),
    }

    # Créer les entités avec les tarifs
    for entity_id in entites_actives:
        base_attrs = {
            "unit_of_measurement": "€",
            "friendly_name": f"[{mode.capitalize()}] {entity_id.split('.')[-1].replace('_', ' ').capitalize()}",
            "source": base_url,
            "integration": "suivi_elec",
            "tarifs": tarifs,  # Ajouter les tarifs comme attributs
        }

        hass.states.async_set(entity_id, "0", base_attrs)

    # Créer une entité pour afficher les tarifs globaux
    hass.states.async_set(
        f"{DOMAIN}.tarifs",
        "Tarifs configurés",
        {
            "kwh": tarifs["kwh"],
            "hp": tarifs["hp"],
            "hc": tarifs["hc"],
            "friendly_name": "Tarifs Suivi Élec",
        },
    )

    return True