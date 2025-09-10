import os
import json
import requests

# 🔐 Lecture directe des variables d’environnement
HA_URL = os.environ.get("HA_URL")
HA_TOKEN = os.environ.get("HA_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json"
}

ENERGY_UNITS = ["kWh", "Wh", "W"]
KEYWORDS = ["energy", "power", "consumption", "electric", "elec"]

def is_energy_entity(entity):
    attrs = entity.get("attributes", {})
    unit = attrs.get("unit_of_measurement", "")
    name = entity.get("entity_id", "").lower()
    return (
        unit in ENERGY_UNITS or
        any(keyword in name for keyword in KEYWORDS)
    )

def get_states():
    url = f"{HA_URL}/api/states"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête : {e}")
        return []

def extract_energy_entities(states):
    return [
        {
            "entity_id": e.get("entity_id"),
            "name": e.get("attributes", {}).get("friendly_name", e.get("entity_id")),
            "unit": e.get("attributes", {}).get("unit_of_measurement", ""),
            "state": e.get("state")
        }
        for e in states if is_energy_entity(e)
    ]

def save_to_file(entities, path="custom_components/suivi_elec/data/capteurs_detectes.json"):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entities, f, indent=2, ensure_ascii=False)
        print(f"✅ Fichier généré : {path} ({len(entities)} entités)")
    except Exception as e:
        print(f"Erreur lors de l’écriture du fichier : {e}")

if __name__ == "__main__":
    if not HA_URL or not HA_TOKEN:
        print("❌ HA_URL ou HA_TOKEN non définis dans les variables d’environnement")
    else:
        states = get_states()
        if states:
            energy_entities = extract_energy_entities(states)
            save_to_file(energy_entities)