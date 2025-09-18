# 📋 Inventaire des tests et configuration

## ✅ Configuration

- `pytest.ini` : limite la détection des tests au dossier `tests/`
- `conftest.py` : charge automatiquement les variables d'environnement depuis `.env`
- `.env` : contient `HA_URL` et `HA_TOKEN` pour les appels API simulés

## 🧪 Tests unitaires

### `test_api_client.py`
- `test_connection_returns_bool` : vérifie que la fonction retourne bien un booléen
- `test_get_energy_entities_with_env` : simule un appel API avec `requests-mock` et vérifie les entités retournées

### `test_detect_utils.py`
- `test_env_variables_loaded` : vérifie que `.env` est bien chargé
- `test_suggest_contract_hp_hc` : détecte le contrat HP/HC
- `test_suggest_contract_prix_unique` : détecte le contrat prix unique

### `test_generation.py`
- `test_generate_yaml_config_basic` : vérifie que le YAML est bien généré
- `test_yaml_contains_main_sections` : vérifie la présence des blocs `sensor`, `input_number`, `template`

## 🧱 Modules ajoutés

- `const.py` : contient les constantes nécessaires à `detect_utils.py`
- `groupes_capteurs_energy.py` : contient les capteurs par pièce pour `generation.py`
- `__init__.py` : rend le dossier `helpers` importable comme package

