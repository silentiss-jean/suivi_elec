# 🗒️ Changelog – Suivi Élec

Ce fichier retrace les évolutions du projet `suivi_elec`, version par version. Les releases sont générées automatiquement via GitHub Actions à partir des tags Git.

---

## v2025.09.10-2015
🔧 **Refonte technique et documentation**
- Ajout d’un dossier `docs/` avec documentation modulaire :
  - `architecture.md`
  - `helpers.md`
  - `components.md`
  - `installation.md`
  - `maintenance.md`
  - `changelog.md`
- Réorganisation complète du `README.md`
- Identification et archivage des modules inutilisés (`check_env.py`, `check_token_direct.py`)
- Nettoyage du dossier `helpers/` et documentation des dépendances internes

---

## v2025.09.01-0930
⚙️ **Améliorations fonctionnelles**
- Ajout du module `generator.py` pour la création d’entités HA
- Refactorisation du module `detect.py` pour simplifier la détection automatique
- Amélioration du calculateur tarifaire (`calculateur.py`)
- Ajout de validations dans `env_loader.py`

---

## v2025.08.20-1500
🚀 **Première version stable**
- Intégration initiale avec `manifest.json`, `__init__.py`, `launcher.py`
- Connexion à l’API fournisseur via `api_client.py`
- Calcul des coûts et mise à jour de l’historique
- Traductions françaises intégrées (`translations/fr.json`)
- Mise en place du workflow GitHub Actions (`release.yml`)