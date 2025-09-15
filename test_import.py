import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
logging.basicConfig()

try:
    from custom_components.suivi_elec.options_flow import SuiviElecOptionsFlow
    print("✅ Import réussi")
except Exception as e:
    print("❌ Erreur à l'import :", e)
