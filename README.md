# Suivi Elec – Intégration Home Assistant

## 🚀 Déploiement via Git + HACS

Cette intégration est publiée automatiquement à chaque `git push` avec un tag `vYYYY.MM.DD-HHMM`.

### 🔧 Workflow

1. Modifiez le code localement
2. Lancez `./update_git.sh`
3. Le script :
   - Commit les changements
   - Crée un tag horodaté
   - Pousse vers GitHub
4. GitHub Actions crée automatiquement une release publique
5. Installez ou mettez à jour via HACS

### 📦 Structure minimale requise

- `custom_components/suivi_elec/__init__.py`
- `manifest.json`
- `launcher.py`
- `helpers/` avec tous les modules nécessaires


📘 [Guide de maintenance](MAINTENANCE.md)
---
