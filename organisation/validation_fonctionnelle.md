# 🔍 Validation fonctionnelle – Intégration Suivi Élec (HACS)

Ce document décrit le fonctionnement attendu de l’intégration Suivi Élec, du point de vue utilisateur Home Assistant via HACS, et les tests associés aux composants critiques.

---

## 🎯 Objectif

Permettre à un utilisateur Home Assistant de :
- Suivre sa consommation énergétique
- Calculer les coûts selon son contrat
- Visualiser les données dans Lovelace
- Exporter les résultats si besoin
- Relancer manuellement la génération si nécessaire

---

## 🧩 Composants principaux

| Composant                  | Rôle                                                                 |
|----------------------------|----------------------------------------------------------------------|
| `.env`                     | Contient `HA_URL` et `HA_TOKEN` requis pour accéder à l’API HA       |
| `detect_async.py`          | Détection automatique à l’installation                               |
| `config_flow.py` / `options_flow.py` | Configuration initiale et options modifiables via UI         |
| `services.yaml`            | Déclenchement manuel du flux via `generate_suivi_elec`               |
| `generation.py`            | Génère les fichiers YAML et Lovelace                                 |
| `export_csv.py`            | Exporte les résultats en CSV                                         |
| `generateur_entites.py`    | Simule des entités pour test local                                   |
| `mise_a_jour_entites.py`   | Synchronise les entités de suivi avec les capteurs source            |

---

## 🪜 Étapes de validation

### 1. ✅ Préparation
- Créer un fichier `.env` avec :
  - `HA_URL=http://...`
  - `HA_TOKEN=...`
- Vérifier que `tarifs.json` est présent et bien formé
- Vérifier que l’API Home Assistant est accessible

### 2. 🚀 Détection automatique
- Installer l’intégration via HACS
- Vérifier que `detect_async.py` est déclenché automatiquement
- Vérifier que les entités énergétiques sont détectées
- Vérifier que `sensor.suivi_elec_status` est créé

### 3. 🧾 Génération YAML + Lovelace
- Appeler le service `generate_suivi_elec`
- Vérifier que les fichiers suivants sont créés :
  - `suivi_elec.yaml`
  - `lovelace_conso.yaml`
  - `lovelace_history_conso.yaml`

### 4. 📤 Export CSV (optionnel)
- Lancer `export_csv.py`
- Vérifier que `cout_estime.csv` est bien généré

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

## 🧪 Modules validés

| Module              | Type de test effectué                                 |
|---------------------|--------------------------------------------------------|
| `detect_utils.py`   | Détection du contrat (prix unique / HP/HC)             |
| `generation.py`     | Structure du YAML généré                               |
| `api_client.py`     | Simulation d’appel API avec `requests-mock`            |
| `config_flow.py`    | Validation du formulaire UI                            |
| `detect_async.py`   | Déclenchement automatique et création du capteur de statut |

---

## 🧪 Modules à tester

| Module                  | Vérification recommandée                            |
|--------------------------|-----------------------------------------------------|
| `services.yaml`          | Appel manuel du service et effet sur les fichiers   |
| `mise_a_jour_entites.py` | Synchronisation correcte des entités                |
| `groupes_capteurs_energy.py` | Cohérence des groupes utilisés dans la génération |

---

## ❌ Modules non testables ou obsolètes

| Module                  | Raison                                               |
|--------------------------|-----------------------------------------------------|
| `check_env.py`           | Redondant avec `env_loader.py`                      |
| `config_flow_toremove.py`| Ancienne version non utilisée                       |

---

## 🧼 Bonnes pratiques

- Ne jamais exposer le token dans les scripts
- Archiver les scripts inutiles (`inutil_*.py`)
- Documenter les fichiers dans `organisation/`
- Utiliser `.env` pour sécuriser les accès API

---

## 🔄 Mise à jour - Septembre 2025

- Intégration complète du flux automatisé via `detect_async.py`
- Ajout du service `generate_suivi_elec` pour relancer manuellement la génération
- Tests unitaires sur les modules critiques
- Documentation technique consolidée dans `organisation/`
