import os
import json
import requests
def load_env(path):
    if not os.path.exists(path):
        print(f"⚠️ Fichier .env non trouvé à {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
    print(f"✅ Variables d’environnement chargées depuis {path}")
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATHS = [
    os.path.join(SCRIPT_DIR, "../../../.env"),
    os.path.join(SCRIPT_DIR, "../.env")
]

for path in ENV_PATHS:
    if os.path.exists(path):
        load_env(path)
        break
    
from datetime import datetime
print("🚀 detect.py lancé")


# 📁 Chemin du log
LOG_PATH = "/config/custom_components/suivi_elec/data/detect.log"
def test_token_validity(url, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(f"{url}/api/", headers=headers, timeout=5)
        if response.status_code == 200:
            print("🔐 Token valide ✅")
            return True
        elif response.status_code == 401:
            print("❌ Token invalide ou expiré (401 Unauthorized)")
        else:
            print(f"⚠️ Réponse inattendue : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur lors du test du token : {e}")
    return False
    
def log(message):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")
# ✅ Maintenant que log() est défini, on peut l’utiliser
log("🚀 detect.py lancé")

def load_env(path):
    if not os.path.exists(path):
        log(f"⚠️ Fichier .env non trouvé à {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
    log(f"✅ Variables d’environnement chargées depuis {path}")

# 📍 Construction dynamique du chemin vers le .env
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, "../../../suivi_elec/.env")
load_env(ENV_PATH)

# 🔐 Lecture des variables
HA_URL = os.environ.get("HA_URL")
HA_TOKEN = os.environ.get("HA_TOKEN")

log(f"HA_URL = {HA_URL}")
log(f"HA_TOKEN = {'présent' if HA_TOKEN else 'absent'}")

if not HA_URL or not HA_TOKEN:
    print("❌ Variables HA_URL ou HA_TOKEN manquantes")
    exit(1)

if not test_token_validity(HA_URL, HA_TOKEN):
    print("🛑 Arrêt du script : token non valide")
    exit(1)

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
        log("✅ Requête API réussie")
        return response.json()
    except requests.exceptions.RequestException as e:
        log(f"❌ Erreur de requête vers {url} : {e}")
        print(f"❌ Erreur de requête : {e}")
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
        log(f"✅ Fichier généré : {path} ({len(entities)} entités)")
        print(f"✅ Fichier généré : {path} ({len(entities)} entités)")
    except Exception as e:
        log(f"❌ Erreur lors de l’écriture du fichier : {e}")
        print(f"❌ Erreur lors de l’écriture du fichier : {e}")

if __name__ == "__main__":
    states = get_states()
    if states:
        energy_entities = extract_energy_entities(states)
        save_to_file(energy_entities)