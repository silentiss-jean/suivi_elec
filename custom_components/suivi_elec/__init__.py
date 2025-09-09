"""Suivi Électrique - Custom Integration."""

import logging
import os
from .launcher import run_all

DOMAIN = "suivi_elec"
_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Initialisation de l'intégration."""
    _LOGGER.debug("[suivi_elec] Initialisation en cours...")

    try:
        run_all(hass)
        _LOGGER.info("[suivi_elec] Lancement réussi.")
    except Exception as e:
        import traceback
        _LOGGER.error(f"[suivi_elec] Erreur au lancement : {e}")
        _LOGGER.debug(traceback.format_exc())
        return False

    # 🧹 Enregistrement du service de nettoyage
    def handle_clean(call):
        paths = [
            "/config/packages/suivi_elec.yaml",
            "/config/packages/lovelace_conso.yaml",
            "/config/packages/lovelace_history_conso.yaml"
        ]
        for path in paths:
            try:
                os.remove(path)
                _LOGGER.info(f"[suivi_elec] Fichier supprimé : {path}")
            except FileNotFoundError:
                _LOGGER.warning(f"[suivi_elec] Fichier introuvable : {path}")
            except Exception as err:
                _LOGGER.error(f"[suivi_elec] Erreur lors de la suppression de {path} : {err}")

    hass.services.register(DOMAIN, "clean", handle_clean)
    _LOGGER.info("[suivi_elec] Service 'clean' enregistré")

    return True