# -*- coding: utf-8 -*-
"""Détection automatique des entités énergétiques à l'installation."""

import logging
from datetime import datetime

from .helpers.api_client import get_energy_entities
from .helpers.calculateur import calculer_cout
from .helpers.historique import update_historique

_LOGGER = logging.getLogger(__name__)

async def run_detect_async(hass, entry):
    _LOGGER.info("🔍 Lancement de la détection automatique (detect_async.py)")

    base_url = entry.data.get("base_url", "http://homeassistant.local:8123")
    token = entry.data.get("token", "")
    mode = entry.data.get("mode", "local")

    tarifs = {
        "type_contrat": entry.data.get("type_contrat", "prix_unique"),
        "prix_ht": entry.data.get("prix_ht", 0.25),
        "prix_ttc": entry.data.get("prix_ttc", 0.30),
        "abonnement_annuel": entry.data.get("abonnement_annuel", 120.0)
    }

    try:
        entites = await get_energy_entities(base_url, token)
        _LOGGER.info("✅ %d entités énergétiques détectées", len(entites))
    except Exception as e:
        _LOGGER.error("❌ Échec de récupération des entités : %s", e)
        entites = []

    couts = []
    for entity in entites:
        try:
            result = calculer_cout(entity, tarifs)
            if result:
                couts.append(result)
        except Exception as e:
            _LOGGER.warning("⚠️ Erreur calcul coût pour %s : %s", entity.get("entity_id"), e)

    _LOGGER.info("💰 Coûts estimés calculés pour %d entités", len(couts))

    for cout in couts:
        try:
            update_historique("data/historique.json", cout["total_ttc"], cout["energie_kwh"])
        except Exception as e:
            _LOGGER.warning("⚠️ Erreur update historique pour %s : %s", cout["entity_id"], e)

    try:
        hass.states.async_set("sensor.suivi_elec_status", f"{mode} | {len(entites)} entités", {
            "mode": mode,
            "source": base_url,
            "entites_actives": [e.get("entity_id") for e in entites],
            "last_update": datetime.now().isoformat()
        })
        _LOGGER.info("🟢 Capteur sensor.suivi_elec_status mis à jour")
    except Exception as e:
        _LOGGER.error("❌ Impossible de créer le capteur de statut : %s", e)

    # 📤 Mise à jour de input_text avec les entités détectées
    try:
        entite_str = ",".join([e.get("entity_id") for e in entites])
        await hass.services.async_call(
            "input_text",
            "set_value",
            {
                "entity_id": "input_text.suivi_elec_entites_detectees",
                "value": entite_str
            },
            blocking=True
        )
        _LOGGER.info("📤 input_text.suivi_elec_entites_detectees mis à jour avec : %s", entite_str)
    except Exception as e:
        _LOGGER.error("❌ Erreur mise à jour input_text : %s", e)
