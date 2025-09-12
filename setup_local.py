import os
import json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SUITELEC_DIR = os.path.join(BASE_DIR, "custom_components", "suivi_elec")
DATA_DIR = os.path.join(SUITELEC_DIR, "data")
ENV_PATH = os.path.join(SUITELEC_DIR, ".env")
TARIF_PATH = os.path.join(DATA_DIR, "tarif.json")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"📁 Dossier créé : {path}")
    else:
        print(f"📁 Dossier déjà présent : {path}")

def ensure_env(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("HA_URL=http://192.168.3.160:8123\nHA_TOKEN=ton_token_ici\n")
        print(f"🔐 Fichier .env créé : {path}")
    else:
        print(f"🔐 Fichier .env déjà présent : {path}")

def ensure_tarif(path):
    if not os.path.exists(path):
        default_tarif = {
            "kwh": 0.1740,
            "hc": 0.1330,
            "hp": 0.2220,
            "abonnement": 11.50
        }
        with open(path, "w") as f:
            json.dump(default_tarif, f, indent=2)
        print(f"💰 Fichier tarif.json créé avec valeurs par défaut : {path}")
    else:
        print(f"💰 Fichier tarif.json déjà présent : {path}")

if __name__ == "__main__":
    print("🔎 Vérification de l’environnement local...")
    ensure_dir(DATA_DIR)
    ensure_env(ENV_PATH)
    ensure_tarif(TARIF_PATH)
    print("✅ Environnement prêt. Tu peux lancer detect.py 🚀")
