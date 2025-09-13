# -*- coding: utf-8 -*-
import os
import json
from random import uniform, choice
from datetime import datetime

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
CAPTEURS_PATH = os.path.join(DATA_DIR, "capteurs_detectes.json")
STATUS_PATH = os.path.join(DATA_DIR, "status_sensor.json")
ENTRY_PATH = os.path.join(DATA_DIR, "entry_data.json")

# Chargement paramètres existants
try:
    with open(ENTRY_PATH, "r") as f:
        entry_data = json.load(f)
except Exception:
    entry_data = {"is_local": True, "base_url": "local"}

mode = "local" if entry_data.get("is_local") else "remote"
base_url = entry_data.get("base_url", "inconnu")

entities = []
n = 10
for i in range(n):
    entity_id = f"sensor.device_{i}_energy"
    state = round(uniform(0.5, 5.0), 2)
    friendly_name = f"Appareil {i}"
    tarif_tag = choice(["hc", "hp", ""])
    full_entity_id = f"{entity_id}_{tarif_tag}" if tarif_tag else entity_id
    entities.append({
        "entity_id": full_entity_id,
        "state": str(state),
        "attributes": {
            "friendly_name": f"[{mode.capitalize()}] {friendly_name}",
            "source": base_url,
            "unit_of_measurement": "kWh"
        }
    })

status_sensor = {
    "entity_id": "sensor.suivi_elec_status",
    "state": f"{mode} | {len(entities)} entités",
    "attributes": {
        "mode": mode,
        "entites_actives": [e["entity_id"] for e in entities],
        "source": base_url,
        "last_update": datetime.now().isoformat()
    }
}

os.makedirs(DATA_DIR, exist_ok=True)
with open(CAPTEURS_PATH, "w", encoding="utf-8") as f:
    json.dump(entities, f, indent=2, ensure_ascii=False)
    print(f"✅ Entités simulées générées : {CAPTEURS_PATH}")

with open(STATUS_PATH, "w", encoding="utf-8") as f:
    json.dump(status_sensor, f, indent=2, ensure_ascii=False)
    print(f"✅ Capteur de statut sauvegardé : {STATUS_PATH}")