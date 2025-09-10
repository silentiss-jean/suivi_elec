import os
import requests

def load_env(path):
    if not os.path.exists(path):
        print(f"❌ Fichier .env introuvable à {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
                print(f"🔑 {key} = {value[:40]}{'...' if len(value) > 40 else ''}")

def test_token(url, token):
    headers = {
    "Authorization": f"Bearer {HA_TOKEN.strip()}",
    "Accept": "application/json"
}

    try:
        response = requests.get(f"{url}/api/", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Token valide, accès à l'API confirmé")
        elif response.status_code == 401:
            print("❌ Token invalide ou expiré (401 Unauthorized)")
        else:
            print(f"⚠️ Réponse inattendue : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de connexion à l'API : {e}")

# 📍 Chemin vers ton .env
ENV_PATH = "/config/suivi_elec/.env"
load_env(ENV_PATH)

HA_URL = os.environ.get("HA_URL")
HA_TOKEN = os.environ.get("HA_TOKEN")

if not HA_URL or not HA_TOKEN:
    print("❌ HA_URL ou HA_TOKEN manquant après chargement")
else:
    test_token(HA_URL, HA_TOKEN)