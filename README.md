# Suivi Élec – Intégration Home Assistant ⚡

Suivi Élec est une intégration personnalisée pour Home Assistant permettant de suivre la consommation énergétique, calculer les coûts, et générer des cartes Lovelace dynamiques.

---

## 📁 Organisation du projet

- `custom_components/suivi_elec/helpers/` → scripts principaux
- `custom_components/suivi_elec/.env` → variables d’environnement (`HA_URL`, `HA_TOKEN`)
- `tests/` → tests unitaires avec `pytest` et `requests-mock`
- `organisation/structure.md` → documentation des scripts
- `organisation/flux_fonctionnel.md` → schéma des interactions
- `organisation/validation_fonctionnelle.md` → couverture des tests
- `organisation/inutilisés.md` → modules non exploités ou en cours d’intégration

---

## 🚀 Fonctionnalités

- Connexion API Home Assistant
- Détection automatique des entités énergétiques
- Calcul du coût selon contrat (prix unique ou HP/HC)
- Historique de consommation
- Génération de fichiers YAML + Lovelace
- Export CSV des résultats
- Simulation d’entités pour test
- Tests unitaires avec simulation d’API

---

## 📚 Pour commencer

1. Crée un fichier `.env` dans `custom_components/suivi_elec/` avec :
HA_URL=http://localhost:8123
HA_TOKEN=your_long_lived_token
2. Lance `detect.py` pour générer les résultats
3. Utilise `generation.py` pour créer les fichiers YAML
4. Consulte les fichiers dans `organisation/` pour comprendre la structure
5. Lance les tests avec :

```bash
python -m pytest -v
🧪 Tests unitaires

•  test_detect_utils.py → détection du contrat (HP/HC ou prix unique)
•  test_generation.py → structure du YAML généré
•  test_api_client.py → simulation d’appel API avec requests-mock
•  Chargement automatique des variables via conftest.py
•  Configuration des tests via pytest.ini

🧠 Documentation

•  structure.md → rôle de chaque script
•  flux_fonctionnel.md → interactions entre modules
•  validation_fonctionnelle.md → couverture des tests
•  inutilisés.md → modules non exploités
🛠️ À venir

•  Interface UI pour configuration
•  Intégration automatique dans Lovelace
•  Support multi-utilisateur
•  Tests d’intégration complets
