# 📊 Suivi Électrique — Intégration Home Assistant

**Suivi Électrique** est une intégration personnalisée pour Home Assistant qui permet de détecter automatiquement les capteurs liés à la consommation électrique, de les regrouper par pièce, et de générer les fichiers YAML et Lovelace nécessaires au suivi énergétique.

---

## 🚀 Fonctionnalités

- 🔍 Détection automatique des capteurs `energy`, `power`, `voltage`, `current`
- 🧠 Regroupement intelligent par pièce via mots-clés ou entités `input_text`
- 🛠 Génération des fichiers :
  - `groupes_capteurs_energy.py`
  - `groupes_capteurs_power.py`
  - `suivi_elec.yaml` (package HA)
  - `lovelace_conso.yaml` (carte par pièce)
  - `lovelace_history_conso.yaml` (historique)

---

## 📦 Installation

1. Copiez le dossier `suivi_elec` dans `/config/custom_components/`
2. Redémarrez Home Assistant
3. Vérifiez que le service `suivi_elec.generate_suivi_elec` est disponible

---

## ⚙️ Utilisation

### 🔧 Via l’interface Home Assistant

1. Allez dans **Outils de développement > Services**
2. Recherchez le service : `suivi_elec.generate_suivi_elec`
3. Cliquez sur **Appeler le service**

### 📁 Fichiers générés

Les fichiers sont créés dans le dossier `data/` du composant :
- `capteurs_detectes.json`
- `groupes_capteurs_energy.py`
- `groupes_capteurs_power.py`
- `suivi_elec.yaml`
- `lovelace_conso.yaml`
- `lovelace_history_conso.yaml`

---

## 🧩 Personnalisation

Vous pouvez personnaliser les regroupements :
- Via le fichier `settings/settings.yaml`
- Ou via des entités `input_text.nom_*` dans Home Assistant

---

## 🛠 Dépendances

- `requests`
- `PyYAML`

---

## 📚 Documentation

À venir sur [GitHub Wiki](https://github.com/silentiss-jean/suivi_elec/wiki)

---

## 📄 Licence

Ce projet est sous licence MIT — libre d’utilisation et de modification.

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Forkez le projet, proposez des améliorations ou ouvrez une issue.

---

## 👤 Auteur

Jean — [github.com/silentiss-jean](https://github.com/silentiss-jean)