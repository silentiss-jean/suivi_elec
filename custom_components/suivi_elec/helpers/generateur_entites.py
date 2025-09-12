import os
import json
from random import uniform, choice

# 📂 Dossier data
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
CAPTEURS_PATH = os.path.join(DATA_DIR, "capteurs_detectes.json")

# 🔧 Génération de capteurs simulés
entities = []
n = 10  # nombre de capteurs simulés

for i in range(n):
    entity_id = f"sensor.device_{i}_energy"
    state = round(uniform(0.5, 5.0), 2)
    friendly_name = f"Appareil {i}"
    tarif_tag = choice(["hc", "hp", ""])

    entities.append({
        "entity_id": entity_id if not tarif_tag else f"{entity_id}_{tarif_tag}",
        "state": str(state),
        "attributes": {
            "friendly_name": friendly_name
        }
    })

# 💾 Sauvegarde
os.makedirs(DATA_DIR, exist_ok=True)
with open(CAPTEURS_PATH, "w") as f:
    json.dump(entities, f, indent=2)
    print(f"✅ Entités simulées générées : {CAPTEURS_PATH}")
