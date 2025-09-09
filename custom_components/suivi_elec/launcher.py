# -*- coding: utf-8 -*-
# Lanceur principal pour générer les fichiers de suivi élec

from .helpers.generation import generate_all

# Exemple de structure de groupes (à adapter selon ton usage réel)
groupes = {
    "Salon": ["sensor.salon_power", "sensor.tv_power"],
    "Cuisine": ["sensor.fridge_power", "sensor.oven_power"]
}

def run_all():
    resultats = generate_all(groupes)

    with open("/data/suivi_elec.yaml", "w", encoding="utf-8") as f:
        f.write(resultats["yaml"])

    with open("/data/lovelace_conso.yaml", "w", encoding="utf-8") as f:
        f.write(resultats["lovelace"])

    with open("/data/lovelace_history_conso.yaml", "w", encoding="utf-8") as f:
        f.write(resultats["history"])

    print("✅ Tous les fichiers ont été générés avec succès.")