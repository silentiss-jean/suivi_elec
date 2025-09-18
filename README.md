# Suivi Élec – Intégration Home Assistant ⚡

Suivi Élec est une intégration personnalisée pour Home Assistant permettant de suivre la consommation énergétique, calculer les coûts, et générer des cartes Lovelace dynamiques.

---

## 📁 Organisation du projet

- `custom_components/suivi_elec/helpers/` → scripts principaux
- `organisation/structure.md` → documentation des scripts
- `organisation/flux_fonctionnel.md` → schéma des interactions

---

## 🚀 Fonctionnalités

- Connexion API Home Assistant
- Détection automatique des entités énergétiques
- Calcul du coût selon contrat (prix unique ou HP/HC)
- Historique de consommation
- Génération de fichiers YAML + Lovelace
- Export CSV des résultats
- Simulation d’entités pour test

---

## 📚 Pour commencer

1. Crée un fichier `.env` avec `HA_URL` et `HA_TOKEN`
2. Lance `detect.py` pour générer les résultats
3. Utilise `generation.py` pour créer les fichiers YAML
4. Consulte les fichiers dans `organisation/` pour comprendre la structure

---

## 🧠 Documentation

- [structure.md](organisation/structure.md) → rôle de chaque script
- [flux_fonctionnel.md](organisation/flux_fonctionnel.md) → interactions entre modules

---

## 🛠️ À venir

- Interface UI pour configuration
- Intégration automatique dans Lovelace
- Support multi-utilisateur