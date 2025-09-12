import logging
import requests

_LOGGER = logging.getLogger(__name__)

def test_api_connection(url: str, token: str) -> bool:
    """Teste la connexion à l'API avec le token fourni."""
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(f"{url}/api/", headers=headers, timeout=5)
        if response.status_code == 200:
            _LOGGER.info("✅ Connexion API réussie")
            return True
        else:
            _LOGGER.warning(f"⚠️ Échec API : {response.status_code}")
            return False
    except Exception as e:
        _LOGGER.error(f"❌ Erreur API : {e}")
        return False

async def test_api_token(token: str, base_url: str) -> bool:
    """Wrapper async pour valider le token via config_flow."""
    return test_api_connection(base_url, token)

def get_energy_entities(url: str, token: str) -> list:
    """Récupère les entités énergétiques (kWh, Wh) depuis l'API HA."""
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(f"{url}/api/states", headers=headers, timeout=10)
        if response.status_code != 200:
            _LOGGER.warning(f"❌ Erreur API /states : {response.status_code}")
            return []

        entities = response.json()
        filtered = []
        for e in entities:
            attrs = e.get("attributes", {})
            if (
                e["entity_id"].startswith("sensor.") and
                attrs.get("unit_of_measurement") in ["kWh", "Wh"] and
                attrs.get("device_class") == "energy"
            ):
                filtered.append({
                    "entity_id": e["entity_id"],
                    "state": e["state"],
                    "unit": attrs.get("unit_of_measurement"),
                    "friendly_name": attrs.get("friendly_name", "")
                })

        _LOGGER.info(f"🔍 {len(filtered)} entités énergétiques détectées")
        return filtered

    except Exception as e:
        _LOGGER.error(f"❌ Erreur récupération entités : {e}")
        return []