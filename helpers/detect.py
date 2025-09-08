import requests
import json

# 🔧 À personnaliser
HA_URL = "http://192.168.3.160:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI5OWUwNDIwNDQyMGU0MTY1OTA3YzcwNDg2MGY5NGYxNCIsImlhdCI6MTc1NzI1NDU5NywiZXhwIjoyMDcyNjE0NTk3fQ.XhrxN8lG4z6CIOPL1P_T6m1qvurHZTBDa6vnrkhvQJ8"

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json"
}

def detect_capteurs():
    response = requests.get(f"{HA_URL}/api/states", headers=HEADERS)
    response.raise_for_status()
    states = response.json()

    capteurs_utiles = []

    for state in states:
        entity_id = state.get("entity_id", "")
        if not entity_id.startswith("sensor."):
            continue

        attrs = state.get("attributes", {})
        device_class = attrs.get("device_class", "")
        unit = attrs.get("unit_of_measurement", "")
        name = attrs.get("friendly_name", entity_id)

        if device_class in ["energy", "power", "current", "voltage"]:
            capteurs_utiles.append({
                "entity_id": entity_id,
                "device_class": device_class,
                "unit_of_measurement": unit,
                "friendly_name": name
            })

    return capteurs_utiles

if __name__ == "__main__":
    capteurs = detect_capteurs()
    with open("/data/capteurs_detectes.json", "w", encoding="utf-8") as f:
        json.dump(capteurs, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(capteurs)} capteurs détectés et enregistrés dans capteurs_detectes.json")