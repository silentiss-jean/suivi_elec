import requests

def test_api_connection(url, token):
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(f"{url}/api/", headers=headers, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erreur API : {e}")
        return False

def get_energy_entities(url, token):
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(f"{url}/api/states", headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Erreur API /states : {response.status_code}")
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
        return filtered
    except Exception as e:
        print(f"❌ Erreur récupération entités : {e}")
        return []