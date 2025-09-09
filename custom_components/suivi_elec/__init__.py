"""Suivi Électrique - Custom Integration."""

import logging
from .launcher import run_all

DOMAIN = "suivi_elec"
_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Initialisation de l'intégration."""
    _LOGGER.debug("[suivi_elec] Initialisation en cours...")
    try:
        run_all(hass)
        _LOGGER.info("[suivi_elec] Lancement réussi.")
        return True
    except Exception as e:
        import traceback
        _LOGGER.error(f"[suivi_elec] Erreur au lancement : {e}")
        _LOGGER.debug(traceback.format_exc())
        return False