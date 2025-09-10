import os
import requests
import json

def load_env(path):
    print(f"📂 Chargement du fichier .env depuis : {path}")
    if not os.path.exists(path):
        print("❌ Fichier .env introuvable")
        return False
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
                print(f"🔑 {key} = {value[:40]}{'...' if len(value) > 40 else ''}")
    return True

def test_token(url, token):
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(f"{url}/api/", headers=headers, timeout=5)
        print(f"📡 Test API : {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return False

def detect_entities(url, token):
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
        filtered = [e for e in entities if "suivi_elec" in e["entity_id"]]
        print(f"🔍 {len(filtered)} entités détectées contenant 'suivi_elec'")
        for e in filtered[:3]:
            print(f"   • {e['entity_id']}")
        return filtered
    except Exception as e:
        print(f"❌ Erreur lors de la détection : {e}")
        return []

def save_entities(entities, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entities, f, indent=2, ensure_ascii=False)
        print(f"📁 {len(entities)} entités enregistrées dans {path}")
    except Exception as e:
        print(f"❌ Erreur lors de l’écriture du fichier : {e}")

# 📍 Chemin vers le .env
ENV_PATH = "/config/suivi_elec/.env"
OUTPUT_PATH = "/config/suivi_elec/capteurs_detectes.json"

if not load_env(ENV_PATH):
    exit(1)

HA_URL = os.environ.get("HA_URL")
HA_TOKEN = os.environ.get("HA_TOKEN")

if not HA_URL or not HA_TOKEN:
    print("❌ HA_URL ou HA_TOKEN manquant")
    exit(1)

if not test_token(HA_URL, HA_TOKEN):
    print("🛑 Token invalide ou API inaccessible")
    exit(1)

print("🚀 detect.py lancé")

entities = detect_entities(HA_URL, HA_TOKEN)
if entities:
    save_entities(entities, OUTPUT_PATH)
else:
    print("⚠️ Aucune entité détectée")