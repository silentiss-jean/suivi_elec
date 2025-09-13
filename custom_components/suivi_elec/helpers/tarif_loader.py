import json
import os

def load_tarifs(path):
    """Charge les tarifs depuis un fichier JSON et valide le format."""
    if not os.path.exists(path):
        print(f"❌ Fichier tarif introuvable : {path}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            tarifs = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lecture tarifs : {e}")
        return None

    if not isinstance(tarifs, dict):
        print(f"❌ Format de tarif invalide : attendu un dictionnaire → {type(tarifs)}")
        return None

    # Vérification minimale des clés attendues
    if not any(k in tarifs for k in ["kwh", "hp", "hc"]):
        print("⚠️ Aucune clé tarifaire standard détectée (kwh, hp, hc)")
    
    print(f"💶 Tarifs chargés : {tarifs}")
    return tarifs