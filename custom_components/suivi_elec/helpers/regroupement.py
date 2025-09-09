import os
import json
import yaml
import requests
from ..config import (
    HA_URL,
    HA_TOKEN,
    FICHIER_CAPTEURS,
    FICHIER_NOMS_PERSONNALISES,
    INPUT_TEXT_ENTITES
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

def ecrit_groupes(groupes, nom_fichier):
    os.makedirs(os.path.dirname(nom_fichier), exist_ok=True)
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write("groupes = {\n")
        for piece, liste in groupes.items():
            f.write(f'    "{piece}": [\n')
            for capteur in liste:
                f.write(f'        "{capteur}",\n')
            f.write("    ],\n")
        f.write("}\n")

def regroupe_capteurs():
    try:
        with open(FICHIER_CAPTEURS, "r", encoding="utf-8") as f:
            capteurs = json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier {FICHIER_CAPTEURS} introuvable.")
        return

    mapping = charger_noms_personnalises()
    groupes_energy = {}
    groupes_power = {}

    for capteur in capteurs:
        entity_id = capteur.get("entity_id", "")
        device_class = capteur.get("device_class", "")
        piece = detect_piece(entity_id, mapping)

        if device_class == "energy":
            groupes_energy.setdefault(piece, []).append(entity_id)
        elif device_class == "power":
            groupes_power.setdefault(piece, []).append(entity_id)

    # 📦 Dossier de l'intégration
    dossier_integration = os.path.dirname(__file__)
    fichier_energy = os.path.join(dossier_integration, "groupes_capteurs_energy.py")
    fichier_power = os.path.join(dossier_integration, "groupes_capteurs_power.py")

    ecrit_groupes(groupes_energy, fichier_energy)
    ecrit_groupes(groupes_power, fichier_power)

    print("✅ Fichiers générés dans le dossier de l'intégration")

if __name__ == "__main__":
    regroupe_capteurs()