# -*- coding: utf-8 -*-
"""Initialisation de l'intégration Suivi Élec."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, ENTITES_POTENTIELLES

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Chargement initial (non utilisé ici)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurer l'intégration Suivi Élec à partir d'une entrée de configuration."""

    mode = entry.data.get("mode", "local")
    base_url = entry.data.get("base_url", "local")
    token = entry.data.get("token", "")  # ✅ Jeton récupéré

    entites_actives = (
        entry.options.get("entites_actives")
        or entry.data.get("entites_actives")
        or ENTITES_POTENTIELLES
    )

    tarifs = {
        "kwh": entry.data.get("prix_ht", 0.15),
        "hp": entry.data.get("prix_ht_hp", 0.18),
        "hc": entry.data.get("prix_ht_hc", 0.12),
    }

    for entity_id in entites_actives:
        base_attrs = {
            "unit_of_measurement": "€",
            "friendly_name": f"[{mode.capitalize()}] {entity_id.split('.')[-1].replace('_', ' ').capitalize()}",
            "source": base_url,
            "integration": DOMAIN,
            "tarifs": tarifs,
            "token": token  # ✅ Jeton ajouté dans les attributs si besoin
        }
        hass.states.async_set(entity_id, "0", base_attrs)

    hass.states.async_set(
        "sensor.suivi_elec_tarifs",
        "Tarifs configurés",
        {
            "kwh": tarifs["kwh"],
            "hp": tarifs["hp"],
            "hc": tarifs["hc"],
            "friendly_name": "Tarifs Suivi Élec",
            "token": token  # ✅ Jeton visible ici aussi si utile
        },
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Déchargement de l'intégration."""
    return True