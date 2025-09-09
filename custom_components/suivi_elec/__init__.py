"""Suivi Électrique - Custom Integration."""

import logging
from .launcher import run_all

DOMAIN = "suivi_elec"
_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Initialisation de l'intégration."""
    try:
        run_all(hass)
        _LOGGER.info("[suivi_elec] Lancement réussi.")
        return True
    except Exception as e:
        _LOGGER.error(f"[suivi_elec] Erreur au lancement : {e}")
        return False