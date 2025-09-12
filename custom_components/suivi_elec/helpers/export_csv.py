import os
import json
import csv

# 📂 Dossier suivi_elec
SUITELEC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(SUITELEC_DIR, "data")

# 📄 Chemins des fichiers
JSON_PATH = os.path.join(DATA_DIR, "cout_estime.json")
CSV_PATH  = os.path.join(DATA_DIR, "cout_estime.csv")

# 📥 Chargement du JSON
try:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print(f"❌ Erreur lecture JSON : {e}")
    exit(1)

resultats = data.get("resultats", [])
if not resultats:
    print("⚠️ Aucun résultat à exporter")
    exit(0)

# 🧾 Export CSV
try:
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "date",
            "entity_id",
            "nom",
            "energie_kwh",
            "prix_kwh",
            "mode_tarif",
            "total_ht",
            "total_ttc"
        ])
        writer.writeheader()
        for r in resultats:
            writer.writerow({
                "date": data.get("date"),
                "entity_id": r.get("entity_id"),
                "nom": r.get("nom"),
                "energie_kwh": r.get("energie_kwh"),
                "prix_kwh": r.get("prix_kwh"),
                "mode_tarif": r.get("mode_tarif"),
                "total_ht": r.get("total_ht"),
                "total_ttc": r.get("total_ttc")
            })
    print(f"✅ Export CSV terminé : {CSV_PATH}")
except Exception as e:
    print(f"❌ Erreur export CSV : {e}")
