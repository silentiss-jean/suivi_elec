import logging
from .helpers import loader

_LOGGER = logging.getLogger(__name__)

def run_all(hass=None):
    groupes = loader.charger_groupes("groupes_capteurs_energy", hass)

    if not groupes:
        _LOGGER.warning("[suivi_elec] Aucun groupe chargé.")
        return

    for groupe in groupes:
        nom = groupe.get("nom")
        capteurs = groupe.get("capteurs")
        _LOGGER.info(f"[suivi_elec] Groupe '{nom}' avec {len(capteurs)} capteurs.")