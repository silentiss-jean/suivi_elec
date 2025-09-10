import json
import os

def load_tarifs(path):
    if not os.path.exists(path):
        print(f"❌ Fichier tarif introuvable : {path}")
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            tarifs = json.load(f)
            print(f"💶 Tarifs chargés : {tarifs}")
            return tarifs
    except Exception as e:
        print(f"❌ Erreur lecture tarifs : {e}")
        return None