import json
import os
from datetime import datetime

def get_keys():
    now = datetime.now()
    jour = now.strftime("%Y-%m-%d")
    semaine = now.strftime("%Y-W%U")
    mois = now.strftime("%Y-%m")
    annee = now.strftime("%Y")
    return jour, semaine, mois, annee

def update_historique(path, total_ttc, energie_kwh):
    jour, semaine, mois, annee = get_keys()
    data = {
        "jour": {},
        "semaine": {},
        "mois": {},
        "annee": {}
    }

    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"⚠️ Erreur lecture historique : {e}")

    def update_section(section, key):
        if key not in data[section]:
            data[section][key] = {
                "total_ttc": 0.0,
                "energie_kwh": 0.0
            }
        data[section][key]["total_ttc"] += round(total_ttc, 4)
        data[section][key]["energie_kwh"] += round(energie_kwh, 4)

    update_section("jour", jour)
    update_section("semaine", semaine)
    update_section("mois", mois)
    update_section("annee", annee)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"🗂️ Historique mis à jour dans {path}")
    except Exception as e:
        print(f"❌ Erreur écriture historique : {e}")