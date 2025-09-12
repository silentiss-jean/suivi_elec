import json
from datetime import datetime
import os

# 📂 Chemins des fichiers
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
CAPTEURS_PATH = os.path.join(DATA_DIR, "capteurs_detectes.json")
STATUS_PATH = os.path.join(DATA_DIR, "status_sensor.json")
ENTRY_PATH = os.path.join(DATA_DIR, "entry_data.json")

# 📥 Chargement des capteurs détectés
try:
    with open(CAPTEURS_PATH, "r") as f:
        capteurs = json.load(f)
except Exception as e:
    print(f"❌ Impossible de charger les capteurs : {e}")
    capteurs = []

# 📦 Chargement des paramètres de configuration
try:
    with open(ENTRY_PATH, "r") as f:
        entry_data = json.load(f)
except Exception as e:
    print(f"⚠️ entry_data.json introuvable ou invalide : {e}")
    entry_data = {}

# 🧠 Détermination du mode
mode = "local" if entry_data.get("is_local") else "distant"
base_url = entry_data.get("base_url", "inconnu")

# 📊 Création des entités
entites_actives = []
for capteur in capteurs:
    entity_id = capteur.get("entity_id")
    if entity_id:
        entite = {
            "entity_id": entity_id,
            "state": capteur.get("state", "unknown"),
            "attributes": {
                "friendly_name": f"[{mode.capitalize()}] {capteur.get('name', entity_id)}",
                "source": base_url,
                "unit_of_measurement": capteur.get("unit", "kWh")
            }
        }
        entites_actives.append(entite)

# 📈 Création du capteur de statut
status_sensor = {
    "entity_id": "sensor.suivi_elec_status",
    "state": f"{mode} | {len(entites_actives)} entités",
    "attributes": {
        "mode": mode,
        "entites_actives": [e["entity_id"] for e in entites_actives],
        "source": base_url,
        "last_update": datetime.now().isoformat()
    }
}

# 💾 Sauvegarde
try:
    with open(STATUS_PATH, "w") as f:
        json.dump(status_sensor, f, indent=2)
        print(f"✅ Capteur de statut sauvegardé : {STATUS_PATH}")
except Exception as e:
    print(f"❌ Erreur lors de la sauvegarde du capteur de statut : {e}")
