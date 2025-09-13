import json

def load_tarifs(filepath):
    """Charge les tarifs depuis un fichier JSON."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except Exception as e:
        raise FileNotFoundError(f"❌ Erreur de lecture du fichier tarif : {e}")

    # Validation minimale
    if not isinstance(data, dict):
        raise ValueError("❌ Format de tarif invalide : attendu un dictionnaire")

    # Exemple attendu :
    # {
    #   "HP": 0.2068,
    #   "HC": 0.1565,
    #   "BASE": 0.1740
    # }

    return data
