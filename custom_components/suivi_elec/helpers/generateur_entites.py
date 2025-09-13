# -*- coding: utf-8 -*-
"""Génère des entités simulées et un capteur de statut pour Suivi Élec."""

import os
import json
from random import uniform, choice
from datetime import datetime

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
CAPTEURS_PATH = os.path.join(DATA_DIR, "capteurs_detectes.json")
STATUS_PATH = os.path.join(DATA_DIR, "status_sensor.json")
ENTRY_PATH = os.path.join(DATA_DIR, "entry_data.json")

# 📄 Création automatique du fichier entry_data.json si absent
if not os.path.exists(ENTRY_PATH):
    default_entry = {
        "is_local": True,
        "base_url": "local",
        "token": "",
        "type_contrat": "prix_unique",
        "prix_ht": 0.2068,
        "abonnement_annuel": 120
    }
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(ENTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(default_entry, f, indent=2, ensure_ascii=False)
        print(f"📄 Fichier entry_data.json créé avec valeurs par défaut : {ENTRY_PATH}")

def charger_entry_data(path):
    """Charge les paramètres d’entrée ou retourne des valeurs par défaut."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Format invalide")
            return data
    except Exception:
        return {"is_local": True, "base_url": "local"}

def generer_entites(n=10, mode="local", base_url="local"):
    """Génère une liste d'entités simulées avec tags tarifaires."""
    entites = []
    for i in range(n):
        entity_id = f"sensor.device_{i}_energy"
        state = round(uniform(0.5, 5.0), 2)
        friendly_name = f"Appareil {i}"
        tarif_tag = choice(["hc", "hp", ""])
        full_entity_id = f"{entity_id}_{tarif_tag}" if tarif_tag else entity_id
        entites.append({
            "entity_id": full_entity_id,
            "state": str(state),
            "timestamp": datetime.now().isoformat(),
            "attributes": {
                "friendly_name": f"[{mode.capitalize()}] {friendly_name}",
                "source": base_url,
                "unit_of_measurement": "kWh"
            }
        })
    return entites

def generer_status(entites, mode, base_url):
    """Crée le capteur de statut global."""
    return {
        "entity_id": "sensor.suivi_elec_status",
        "state": f"{mode} | {len(entites)} entités",
        "attributes": {
            "mode": mode,
            "entites_actives": [e["entity_id"] for e in entites],
            "source": base_url,
            "last_update": datetime.now().isoformat()
        }
    }

def main():
    entry_data = charger_entry_data(ENTRY_PATH)
    mode = "local" if entry_data.get("is_local") else "remote"
    base_url = entry_data.get("base_url", "inconnu")

    entites = generer_entites(n=10, mode=mode, base_url=base_url)
    status_sensor = generer_status(entites, mode, base_url)

    with open(CAPTEURS_PATH, "w", encoding="utf-8") as f:
        json.dump(entites, f, indent=2, ensure_ascii=False)
        print(f"✅ Entités simulées générées : {CAPTEURS_PATH}")

    with open(STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(status_sensor, f, indent=2, ensure_ascii=False)
        print(f"✅ Capteur de statut sauvegardé : {STATUS_PATH}")

if __name__ == "__main__":
    main()