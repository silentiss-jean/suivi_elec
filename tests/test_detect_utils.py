import os
from custom_components.suivi_elec.helpers.detect_utils import suggest_contract

def test_env_variables_loaded():
    """Vérifie que les variables d'environnement sont bien chargées depuis .env."""
    assert os.getenv("HA_URL") is not None
    assert os.getenv("HA_TOKEN") is not None

def test_suggest_contract_hp_hc():
    entities = ["sensor.device_hp", "sensor.device_hc"]
    assert suggest_contract(entities) == "heures_pleines_creuses"

def test_suggest_contract_prix_unique():
    entities = ["sensor.device_energy"]
    assert suggest_contract(entities) == "prix_unique"
