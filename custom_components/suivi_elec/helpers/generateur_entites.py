import os
import json
import yaml
import requests
from ..config import (
    HA_URL,
    HA_TOKEN,
    FICHIER_CAPTEURS,
    FICHIER_NOMS_PERSONNALISES,
    INPUT_TEXT_ENTITES,
    FICHIER_MAPPING_SUIVI_ELEC
)

def charger_noms_personnalises():
    mapping = {}
    headers = {"Authorization": f"Bearer {HA_TOKEN}"}
    for entite in INPUT_TEXT_ENTITES:
        try:
            r = requests.get(f"{HA_URL}/api/states/{entite}", headers=headers)
            if r.status_code == 200:
                cle = entite.replace("input_text.nom_", "")
                mapping[cle] = r.json()["state"]
        except Exception:
            pass

    try:
        with open(FICHIER_NOMS_PERSONNALISES, "r", encoding="utf-8") as f:
            yaml_mapping = yaml.safe_load(f) or {}
            for mot_cle, nom_final in yaml_mapping.items():
                if mot_cle not in mapping:
                    mapping[mot_cle] = nom_final
    except FileNotFoundError:
        pass

    return mapping

def detect_piece(nom_capteur, mapping):
    for mot_cle, nom_final in mapping.items():
        if mot_cle.lower() in nom_capteur.lower():
            return nom_final
    return "Autres"

def genere_nom_suivi_elec(piece, type_capteur):
    return f"sensor.suivi_elec_{piece.lower()}_{type_capteur.lower()}"

def injecte_entite(entity_id, source_id, piece, device_class, unit):
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "state": "0",
        "attributes": {
            "source": source_id,
            "integration": "suivi_elec",
            "device_class": device_class,
            "unit_of_measurement": unit,
            "piece": piece
        }
    }
    try:
        r = requests.post(f"{HA_URL}/api/states/{entity_id}", headers=headers, json=payload)
        if r.status_code == 200:
            print(f"✅ Entité injectée : {entity_id}")
        else:
            print(f"❌ Erreur lors de l'injection de {entity_id} : {r.status_code}")
    except Exception as e:
        print(f"❌ Exception : {e}")

def genere_entites_suivi_elec():
    try:
        with open(FICHIER_CAPTEURS, "r", encoding="utf-8") as f:
            capteurs = json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier {FICHIER_CAPTEURS} introuvable.")
        return

    mapping = charger_noms_personnalises()
    suivi_elec_mapping = {}

    for capteur in capteurs:
        entity_id = capteur.get("entity_id", "")
        device_class = capteur.get("device_class", "")
        unit = capteur.get("unit_of_measurement", "")
        piece = detect_piece(entity_id, mapping)

        if device_class in ["energy", "power"]:
            type_capteur = "conso" if device_class == "energy" else "puissance"
            nom_suivi_elec = genere_nom_suivi_elec(piece, type_capteur)

            injecte_entite(nom_suivi_elec, entity_id, piece, device_class, unit)

            suivi_elec_mapping.setdefault(piece, {})[type_capteur] = {
                "source": entity_id,
                "suivi_elec": nom_suivi_elec
            }

    # Sauvegarde du mapping
    os.makedirs(os.path.dirname(FICHIER_MAPPING_SUIVI_ELEC), exist_ok=True)
    with open(FICHIER_MAPPING_SUIVI_ELEC, "w", encoding="utf-8") as f:
        json.dump(suivi_elec_mapping, f, indent=4, ensure_ascii=False)

    print("📦 Mapping Suivi Élec sauvegardé.")

if __name__ == "__main__":
    genere_entites_suivi_elec()