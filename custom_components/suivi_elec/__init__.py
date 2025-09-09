"""Suivi Électrique - Custom Integration."""
DOMAIN = "suivi_elec"

def setup(hass, config):
    """Initialisation de l'intégration."""
    try:
        from .launcher import run_all
        run_all()
        return True
    except Exception as e:
        # Log l'erreur dans Home Assistant
        hass.components.logger.error(f"[suivi_elec] Erreur au lancement : {e}")
        return False