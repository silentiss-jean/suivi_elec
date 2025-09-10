# 🧱 Architecture du projet `suivi_elec`

Ce document décrit l’organisation technique de l’intégration Home Assistant `suivi_elec`, ses composants principaux, et leurs interactions.

---

## 📦 Structure générale

```text
suivi_elec/
├── custom_components/
│   └── suivi_elec/
│       ├── __init__.py
│       ├── manifest.json
│       ├── launcher.py
│       ├── generator.py
│       ├── helpers/
│       └── translations/
├── .github/
│   └── workflows/
├── update_git.sh
├── README.md
├── docs/
│   └── architecture.md