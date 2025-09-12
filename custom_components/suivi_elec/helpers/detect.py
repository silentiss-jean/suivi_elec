import os
import sys
import json
from datetime import datetime

# 📦 Ajout du dossier helpers au path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from helpers.env_loader import load_env
from helpers.api_client import test_api_connection, get_energy_entities
from helpers.tarif_loader import load_tarifs
from helpers.calculateur import calculer_cout
from helpers.historique import update_historique

# 📂 Dossier suivi_elec
SUITELEC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(SUITELEC_DIR, "data")

# 📄 Chemins des fichiers
ENV_PATH       = os.path.join(SUITELEC_DIR, ".env")
TARIF_PATH     = os.path.join(DATA_DIR, "tarif.json")
OUTPUT_PATH    = os.path.join(DATA_DIR, "cout_estime.json")
HISTO_PATH     = os.path.join(DATA_DIR, "historique_cout.json")
CAPTEURS_PATH  = os.path.join(DATA_DIR, "capteurs_detectes.json")

# 🔧 Chargement des variables d’environnement
print(f"📂 Chargement du fichier .env depuis : {ENV_PATH}")
if not load_env(ENV_PATH):
    print("❌ Fichier .env introuvable ou invalide")
    exit(1)

# 🔑 Récupération des variables
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

if not HA_URL or not HA_TOKEN:
    print("❌ HA_URL ou HA_TOKEN manquant")
    exit(1)

print(f"🔑 HA_URL = {HA_URL}")
print(f"🔑 HA_TOKEN = {HA_TOKEN}")
print("🚀 detect.py lancé")

# 🔍 Test de connexion à l'API
if not test_api_connection(HA_URL, HA_TOKEN):
    print("❌ Connexion à Home Assistant échouée")
    exit(1)

# 🔋 Récupération des entités énergétiques
entities = get_energy_entities(HA_URL, HA_TOKEN)
print(f"🔋 {len(entities)} entités énergétiques détectées")

# 💾 Sauvegarde des capteurs détectés
try:
    with open(CAPTEURS_PATH, "w") as f:
        json.dump(entities, f, indent=2)
        print(f"✅ Fichier capteurs détectés sauvegardé : {CAPTEURS_PATH}")
except Exception as e:
    print(f"❌ Erreur lors de la sauvegarde des capteurs : {e}")

# 💰 Chargement des tarifs
try:
    tarifs = load_tarifs(TARIF_PATH)
    print(f"💶 Tarifs chargés : {tarifs}")
except FileNotFoundError:
    print(f"❌ Fichier tarif introuvable : {TARIF_PATH}")
    tarifs = None

# 📊 Calcul du coût estimé
resultats = []
if tarifs:
    for entity in entities:
        try:
            cout = calculer_cout(entity, tarifs)
            if cout:
                resultats.append(cout)
        except Exception as e:
            print(f"⚠️ Ignoré {entity.get('entity_id', 'inconnu')} → {e}")

    # 🧮 Résumé global
    total_ttc = sum(r["total_ttc"] for r in resultats)
    energie_kwh = sum(r["energie_kwh"] for r in resultats)

    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_kwh": round(energie_kwh, 2),
        "total_ttc": round(total_ttc, 2),
        "resultats": resultats
    }

    try:
        with open(OUTPUT_PATH, "w") as f:
            json.dump(output, f, indent=2)
            print(f"✅ Coût estimé sauvegardé : {OUTPUT_PATH}")
        update_historique(HISTO_PATH, total_ttc, energie_kwh)
        print(f"📈 Historique mis à jour : {HISTO_PATH}")
    except Exception as e:
        print(f"❌ Erreur lors de l’écriture du coût ou de l’historique : {e}")
else:
    print("⚠️ Tarifs non disponibles, coût non calculé")
