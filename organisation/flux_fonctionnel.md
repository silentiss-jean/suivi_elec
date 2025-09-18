# Flux fonctionnel de l'intégration Suivi Élec

Ce fichier décrit les interactions entre les différents modules de `helpers/`.

---

## 🔄 Schéma général
.env → env_loader.py
   
HA_URL + HA_TOKEN → api_client.py → test connexion + récupération des entités
   
tarif_loader.py → charge les tarifs
   
detect.py → utilise :
    - api_clien
    - calculateu
    - historiqu
    - tarif_loade
    - env_loade
   
    → génère cout_estime.
   
export_csv.py → transforme en cout_estime.csv

---

## 🧠 Modules intelligents

- `detect_utils.py` → détecte le mode, les entités, et suggère un contrat
- `entity_selector.py` → compare les entités existantes vs potentielles

---

## 🧪 Modules de simulation

- `generateur_entites.py` → génère des entités fictives
- `mise_a_jour_entites.py` → synchronise les entités de suivi avec les capteurs source

---

## 🧱 Modules de structure

- `regroupement.py` → regroupe les capteurs par pièce
- `loader.py` → charge dynamiquement les groupes
- `generation.py` → génère YAML + Lovelace + historique

---

## 🗑️ Modules à archiver

- `check_env.py`
- `check_token_direct.py`
- `config_flow_toremove.py`