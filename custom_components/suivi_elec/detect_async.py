import os
import json
import logging
from datetime import datetime
from homeassistant.core import HomeAssistant

from .helpers.env_loader import load_env
from .helpers.api_client import test_api_connection, get_energy_entities
from .helpers.tarif_loader import load_tarifs
from .helpers.calculateur import calculer_cout
from .helpers.historique import update_historique

_LOGGER = logging.getLogger(__name__)

async def async_detect_and_store(hass: HomeAssistant, env_path: str, data_dir: str):
    if not load_env(env_path):
        _LOGGER.error("Fichier .env introuvable ou invalide")
        return

    ha_url = os.getenv("HA_URL")
    ha_token = os.getenv("HA_TOKEN")

    if not ha_url or not ha_token:
        _LOGGER.error("HA_URL ou HA_TOKEN manquant")
        return

    _LOGGER.info(f"Connexion à Home Assistant : {ha_url}")

    if not test_api_connection(ha_url, ha_token):
        _LOGGER.error("Connexion à Home Assistant échouée")
        return

    entities = get_energy_entities(ha_url, ha_token)
    entity_ids = [e["entity_id"] for e in entities]
    _LOGGER.info(f"{len(entity_ids)} entités énergétiques détectées")

    hass.states.async_set("input_text.suivi_elec_entites_detectees", ",".join(entity_ids))

    capteurs_path = os.path.join(data_dir, "capteurs_detectes.json")
    with open(capteurs_path, "w") as f:
        json.dump(entities, f, indent=2)
        _LOGGER.info(f"Capteurs sauvegardés dans {capteurs_path}")

    tarif_path = os.path.join(data_dir, "tarif.json")
    try:
        tarifs = load_tarifs(tarif_path)
    except FileNotFoundError:
        _LOGGER.warning(f"Fichier tarif introuvable : {tarif_path}")
        tarifs = None

    resultats = []
    if tarifs:
        for entity in entities:
            try:
                cout = calculer_cout(entity, tarifs)
                if cout:
                    resultats.append(cout)
            except Exception as e:
                _LOGGER.warning(f"Ignoré {entity.get('entity_id', 'inconnu')} → {e}")

        total_ttc = sum(r["total_ttc"] for r in resultats)
        energie_kwh = sum(r["energie_kwh"] for r in resultats)

        output = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_kwh": round(energie_kwh, 2),
            "total_ttc": round(total_ttc, 2),
            "resultats": resultats
        }

        output_path = os.path.join(data_dir, "cout_estime.json")
        with open(output_path, "w") as f:
            json.dump(output, f, indent=2)
            _LOGGER.info(f"Coût estimé sauvegardé dans {output_path}")

        histo_path = os.path.join(data_dir, "historique_cout.json")
        update_historique(histo_path, total_ttc, energie_kwh)
        _LOGGER.info(f"Historique mis à jour dans {histo_path}")
    else:
        _LOGGER.warning("Tarifs non disponibles, coût non calculé")