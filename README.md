# ⚡ Suivi Élec – Intégration Home Assistant

**Suivi Élec** est une intégration personnalisée pour Home Assistant permettant de suivre votre consommation électrique, vos tarifs, et vos historiques de manière automatisée et intelligente.

---

## 📑 Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Structure du projet](#structure-du-projet)
- [Documentation technique](#documentation-technique)
- [Maintenance](#maintenance)
- [Historique des versions](docs/changelog.md)
- [Contribuer](#contribuer)
- [Feuille de route du projet](docs/roadmap.md)
- [Licence](#licence)
- [Auteur](#auteur)

---

## 🚀 Fonctionnalités

- Détection automatique des entités liées à l’électricité
- Connexion à l’API fournisseur (ex. EDF)
- Calcul des coûts énergétiques en fonction des tarifs
- Mise à jour de l’historique de consommation
- Traductions intégrées pour l’interface Home Assistant

---

## 🛠️ Installation

### Via HACS (recommandé)

1. Ajouter ce dépôt comme dépôt personnalisé dans HACS
2. Installer l’intégration `suivi_elec`
3. Redémarrer Home Assistant
4. Configurer via l’interface ou fichier YAML

### Manuellement via Git

```bash
cd custom_components/
git clone https://github.com/silentiss-jean/suivi_elec.git
📁 Structure du projet
suivi_elec/ ├── custom_components/ │ └── suivi_elec/ │ ├── init.py │ ├── manifest.json │ ├── launcher.py │ ├── generator.py │ ├── helpers/ │ └── translations/ ├── .github/ │ └── workflows/ ├── update_git.sh ├── README.md ├── docs/

📚 Documentation technique
• Composants principaux
• Modules utilitaires (helpers/)
• Installation détaillée
• Maintenance & mise à jour

➡️ Voir docs/maintenance.md

🔧 Maintenance
• Releases automatisées via GitHub Actions
• Script local update_git.sh (optionnel)
• Nettoyage régulier des fichiers inutilisés

📄 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus d’informations.

👤 Auteur
Jean · GitHub @silentiss-jean

Dernière mise à jour : 13 septembre 2025
