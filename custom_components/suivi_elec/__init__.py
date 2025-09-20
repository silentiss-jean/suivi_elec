# -*- coding: utf-8 -*-
"""Initialisation de l'intégration Suivi Élec."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, ENTITES_POTENTIELLES
from .detect_async import run_detect_async

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Chargement initial (non utilisé ici)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurer l'intégration Suivi Élec à partir d'une entrée de configuration."""

    data = entry.data
    options = entry.options

    mode = data.get("mode", "local")
    base_url = data.get("base_url", "local")
    token = data.get("token", "")
    type_contrat = data.get("type_contrat", "prix_unique")

    entites_actives = (
        options.get("entites_actives")
        or data.get("entites_actives")
        or ENTITES_POTENTIELLES
    )

    if type_contrat == "prix_unique":
        tarifs = {
            "kwh": data.get("prix_ht", 0.15),
            "hp": data.get("prix_ht", 0.15),
            "hc": data.get("prix_ht", 0.15),
        }
    else:
        tarifs = {
            "kwh": data.get("prix_ht_hp", 0.18),
            "hp": data.get("prix_ht_hp", 0.18),
            "hc": data.get("prix_ht_hc", 0.12),
        }

    abonnement = data.get("abonnement_annuel", 0.0)

    for entity_id in entites_actives:
        base_attrs = {
            "unit_of_measurement": "€",
            "friendly_name": f"[{mode.capitalize()}] {entity_id.split('.')[-1].replace('_', ' ').capitalize()}",
            "source": base_url,
            "integration": DOMAIN,
            "tarifs": tarifs,
            "abonnement_annuel": abonnement
            # ❌ token supprimé pour éviter l'exposition
        }
        hass.states.async_set(entity_id, "0", base_attrs)

    hass.states.async_set(
        "sensor.suivi_elec_tarifs",
        "Tarifs configurés",
        {
            "kwh": tarifs["kwh"],
            "hp": tarifs["hp"],
            "hc": tarifs["hc"],
            "abonnement_annuel": abonnement,
            "friendly_name": "Tarifs Suivi Élec",
            "mode": mode  # ✅ Ajout explicite du mode ici aussi
        },
    )

    # 🚀 Détection automatique des entités énergétiques
    await run_detect_async(hass, entry)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Déchargement de l’intégration."""
    return True
