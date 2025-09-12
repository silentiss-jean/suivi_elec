import os
import json
import requests
from ..config import HA_URL, HA_TOKEN, FICHIER_MAPPING_SUIVI_ELEC

def get_etat_entite(entity_id):
    headers = {"Authorization": f"Bearer {HA_TOKEN}"}
    try:
        r = requests.get(f"{HA_URL}/api/states/{entity_id}", headers=headers)
        if r.status_code == 200:
            return r.json()["state"]
        else:
            print(f"❌ Erreur GET {entity_id} : {r.status_code}")
    except Exception as e:
        print(f"❌ Exception GET {entity_id} : {e}")
    return None

def update_entite_suivi_elec(entity_id, valeur, attributs):
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "state": valeur,
        "attributes": attributs
    }
    try:
        r = requests.post(f"{HA_URL}/api/states/{entity_id}", headers=headers, json=payload)
        if r.status_code == 200:
            print(f"✅ Mise à jour : {entity_id} ← {valeur}")
        else:
            print(f"❌ Erreur POST {entity_id} : {r.status_code}")
    except Exception as e:
        print(f"❌ Exception POST {entity_id} : {e}")

def mise_a_jour_entites():
    if not os.path.exists(FICHIER_MAPPING_SUIVI_ELEC):
        print(f"❌ Mapping introuvable : {FICHIER_MAPPING_SUIVI_ELEC}")
        return

    with open(FICHIER_MAPPING_SUIVI_ELEC, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    for piece, types in mapping.items():
        for type_capteur, infos in types.items():
            source_id = infos.get("source")
            suivi_elec_id = infos.get("suivi_elec")

            valeur = get_etat_entite(source_id)
            if valeur is None:
                continue

            # Reprendre les attributs existants
            headers = {"Authorization": f"Bearer {HA_TOKEN}"}
            r = requests.get(f"{HA_URL}/api/states/{suivi_elec_id}", headers=headers)
            if r.status_code == 200:
                attributs = r.json().get("attributes", {})
            else:
                attributs = {
                    "source": source_id,
                    "integration": "suivi_elec",
                    "piece": piece,
                    "type": type_capteur
                }

            update_entite_suivi_elec(suivi_elec_id, valeur, attributs)

if __name__ == "__main__":
    mise_a_jour_entites()
