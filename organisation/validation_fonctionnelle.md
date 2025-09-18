# 🔍 Validation fonctionnelle – Intégration Suivi Élec (HACS)

Ce document décrit le fonctionnement attendu de l’intégration Suivi Élec, en partant du bon côté : celui de l’utilisateur Home Assistant via HACS.

---

## 🎯 Objectif

Permettre à un utilisateur Home Assistant de :
- Suivre sa consommation énergétique
- Calculer les coûts selon son contrat
- Visualiser les données dans Lovelace
- Exporter les résultats si besoin

---

## 🧩 Composants principaux

| Composant              | Rôle                                                                 |
|------------------------|----------------------------------------------------------------------|
| `.env`                 | Contient `HA_URL` et `HA_TOKEN` requis pour accéder à l’API HA       |
| `detect.py`            | Script principal : détecte les entités, calcule les coûts, met à jour l’historique |
| `generation.py`        | Génère les fichiers YAML et Lovelace                                 |
| `export_csv.py`        | Exporte les résultats en CSV                                         |
| `generateur_entites.py`| Simule des entités pour test local                                   |
| `mise_a_jour_entites.py`| Synchronise les entités de suivi avec les capteurs source           |

---

## 🪜 Étapes de validation

### 1. ✅ Préparation
- Créer un fichier `.env` avec :
  - `HA_URL=http://...`
  - `HA_TOKEN=...`
- Vérifier que `tarifs.json` est présent et bien formé
- Vérifier que l’API Home Assistant est accessible

### 2. 🚀 Lancer `detect.py`
- Charge les variables d’environnement
- Teste la connexion à HA
- Récupère les entités énergétiques
- Calcule les coûts via `calculateur.py`
- Met à jour l’historique via `historique.py`
- Génère `cout_estime.json`

### 3. 📤 Export CSV (optionnel)
- Lancer `export_csv.py`
- Vérifier que `cout_estime.csv` est bien généré

### 4. 🧾 Génération YAML + Lovelace
- Lancer `generation.py`
- Vérifier que les fichiers suivants sont créés :
  - `suivi_elec.yaml`
  - `lovelace_conso.yaml`
  - `lovelace_history_conso.yaml`

### 5. 🧪 Simulation (optionnel)
- Lancer `generateur_entites.py` pour créer des entités fictives
- Lancer `mise_a_jour_entites.py` pour synchroniser les entités de suivi

---

## 🧠 Fonctionnement attendu dans Home Assistant

- L’utilisateur installe l’intégration via HACS
- Il configure son contrat (prix unique ou HP/HC)
- Les entités sont détectées automatiquement
- Les coûts sont calculés et affichés dans Lovelace
- L’historique est mis à jour chaque jour
- L’utilisateur peut exporter les résultats si besoin

---

## 🧼 Bonnes pratiques

- Ne jamais exposer le token dans les scripts
- Archiver les scripts inutiles (`inutil_*.py`)
- Documenter les fichiers dans `organisation/`

---

## 🔄 Mise à jour - Septembre 2025

- Ajout de tests unitaires sur :
  - `detect_utils.py` : détection du contrat (HP/HC ou prix unique)
  - `generation.py` : structure du YAML généré
  - `api_client.py` : simulation d’appel API avec `requests-mock`
- Utilisation de `.env` pour sécuriser les accès API
- Couverture des fonctions critiques sans modifier le code métier
