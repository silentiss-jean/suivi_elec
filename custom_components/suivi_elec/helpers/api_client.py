import requests

HEADERS_TEMPLATE = {
    "Authorization": "Bearer {token}",
    "Content-Type": "application/json"
}

def test_api_connection(base_url, token):
    """Teste la connexion à l'API Home Assistant."""
    url = f"{base_url}/api/"
    headers = HEADERS_TEMPLATE.copy()
    headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erreur de connexion à l'API : {e}")
        return False


def get_energy_entities(base_url, token):
    """Récupère les entités énergétiques depuis Home Assistant."""
    url = f"{base_url}/api/states"
    headers = HEADERS_TEMPLATE.copy()
    headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        all_entities = response.json()
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des entités : {e}")
        return []

    # Filtrage des entités énergétiques
    energy_entities = []
    for entity in all_entities:
        entity_id = entity.get("entity_id", "")
        if entity_id.startswith("sensor.") and "kwh" in str(entity.get("state", "")).lower():
            energy_entities.append({
                "entity_id": entity_id,
                "state": entity.get("state"),
                "name": entity.get("attributes", {}).get("friendly_name", entity_id),
                "unit": entity.get("attributes", {}).get("unit_of_measurement", "kWh")
            })

    return energy_entities
