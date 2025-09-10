import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import json
from datetime import datetime

from helpers.env_loader import load_env
from helpers.api_client import test_api_connection, get_energy_entities
from helpers.tarif_loader import load_tarifs
from helpers.calculateur import calculer_cout
from helpers.historique import update_historique

# 📍 Chemins
ENV_PATH = "/config/suivi_elec/.env"
TARIF_PATH = "/config/suivi_elec/tarif.json"
OUTPUT_PATH = "/config/suivi_elec/cout_estime.json"
HISTO_PATH = "/config/suivi_elec/historique_cout.json"

# 🔧 Chargement des variables d’environnement
if not load_env(ENV_PATH):
    exit(1)

HA_URL = os.environ.get("HA_URL")
HA_TOKEN = os.environ.get("HA_TOKEN")

if not HA_URL or not HA_TOKEN:
    print("❌ HA_URL ou HA_TOKEN manquant")
    exit(1)

# 🌐 Vérification de l’accès à l’API
if not test_api_connection(HA_URL, HA_TOKEN):
    print("🛑 Token invalide ou API inaccessible")
    exit(1)

print("🚀 detect.py lancé")

# 🔍 Récupération des entités énergétiques
entities = get_energy_entities(HA_URL, HA_TOKEN)
if not entities:
    print("⚠️ Aucune entité énergétique détectée")
    exit(1)

print(f"🔋 {len(entities)} entités énergétiques détectées")

# 💶 Chargement des tarifs
tarifs = load_tarifs(TARIF_PATH)
if not tarifs:
    print("❌ Tarifs non disponibles")
    exit(1)

# 🧮 Calcul des coûts
resultats = []
for entity in entities:
    cout = calculer_cout(entity, tarifs)
    if cout:
        resultats.append(cout)

# 🕰️ Ajout de la date
date_str = datetime.now().strftime("%Y-%m-%d")
output = {
    "date": date_str,
    "resultats": resultats
}

# 📁 Sauvegarde du fichier de coût estimé
try:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"📁 Coût estimé enregistré dans {OUTPUT_PATH}")
except Exception as e:
    print(f"❌ Erreur lors de l’écriture du fichier : {e}")

# 🗂️ Mise à jour de l’historique
total_ttc = sum(r["total_ttc"] for r in resultats)
energie_kwh = sum(r["energie_kwh"] for r in resultats)

update_historique(HISTO_PATH, total_ttc, energie_kwh)