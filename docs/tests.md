# 🧪 Cas de test — Modules Python `suivi_elec`

Ce fichier regroupe les cas de test unitaires et fonctionnels pour les modules du dossier `helpers/`. Il permet de valider le bon fonctionnement de chaque composant, notamment en cas de modification ou de refactoring.

---

## 🔧 `api_client.py`

### `test_api_connection(base_url, token)`
- ✅ Connexion valide → retourne `True`
- ❌ Jeton invalide → retourne `False`
- ❌ URL inaccessible → retourne `False`

### `get_energy_entities(base_url, token)`
- ✅ Entités avec `unit_of_measurement = "kWh"` → filtrées correctement
- ❌ Jeton invalide → retourne liste vide ou erreur
- ❌ Réponse mal formée → gérée sans crash

---

## 💶 `tarif_loader.py`

### `load_tarifs(path)`
- ✅ Fichier bien formé → retourne un `dict`
- ❌ Fichier absent → retourne `None`, affiche erreur
- ❌ Fichier mal formé → retourne `None`, affiche erreur
- ❌ Format non dict → retourne `None`, affiche erreur
- ⚠️ Clés manquantes (`hp`, `hc`, `kwh`) → avertissement

---

## 🧮 `calculateur.py`

### `calculer_cout(entity, tarifs)`
- ✅ Entité avec valeur numérique → retourne dict complet
- ❌ `state = "unknown"` ou `"unavailable"` → retourne `None`
- ❌ `state` non convertible → retourne `None`
- ✅ Tarif `hp` ou `hc` → détecté via `entity_id`
- ❌ Tarif manquant → fallback sur `tarifs["kwh"]`
- ✅ Calcul HT + TVA → total cohérent

---

## 📈 `historique.py`

### `update_historique(filepath, total_ttc, total_kwh)`
- ✅ Fichier existant → ajoute une ligne avec date du jour
- ❌ Fichier absent → crée un nouveau fichier
- ❌ Fichier corrompu → affiche erreur
- ✅ Format JSON respecté → liste de dicts

---

## 🧪 À venir

- Tests pour `generateur_entities.py`
- Tests d’intégration avec `detect.py`
- Tests simulés avec faux jeton / fausse API

