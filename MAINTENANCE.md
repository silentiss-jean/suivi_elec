# 🛠️ Maintenance du composant `suivi_elec`

Ce document décrit le processus complet pour maintenir, publier et distribuer l’intégration `suivi_elec` via GitHub et HACS, sans copie manuelle.

---

## 🔄 Mise à jour du code

1. Modifier les fichiers dans `custom_components/suivi_elec/` selon les évolutions souhaitées.
2. Lancer le script :
   ```bash
   ./update_git.sh

Ce script :

•  ✅ Vérifie que les fichiers critiques sont présents :
  ⁠◦  __init__.py
  ⁠◦  manifest.json
  ⁠◦  launcher.py
  ⁠◦  helpers/detect.py
•  📦 Commit les modifications locales avec un message horodaté
•  🏷️ Crée un tag au format vYYYY.MM.DD-HHMM (exemple : v2025.09.09-1320)
•  🚀 Pousse le commit et le tag vers GitHub
•  🧠 Déclenche automatiquement une release via GitHub Actions

🚀 Publication automatique via GitHub Actions

Une fois le tag poussé, une release GitHub est automatiquement créée grâce au workflow défini dans .github/workflows/release.yml. Ce workflow utilise l’action softprops/action-gh-release pour publier la release sans intervention manuelle.

Il n’est plus nécessaire d’aller sur GitHub pour cliquer “Publish release” — tout est automatisé.

📥 Installation via HACS

HACS installe uniquement les versions publiées en release. Une fois la release créée :

•  Ouvrir Home Assistant
•  Aller dans HACS → Intégrations → suivi_elec
•  Cliquer sur "Mise à jour disponible" ou "Reinstall"
•  Redémarrer Home Assistant si nécessaire

🧪 Tests et débogage

Après chaque mise à jour :
Redémarrer Home Assistant :
ha core restart
Vérifier les logs dans l’interface ou via SSH :
ha core logs
Erreurs fréquentes :

•  Fichier manquant dans la release
•  Mauvais nom d’intégration dans configuration.yaml
•  Import cassé dans un module Python

🧠 Bonnes pratiques

•  Ne jamais copier manuellement dans /custom_components
•  Toujours passer par Git + HACS pour la distribution
•  Taguer chaque version avec un horodatage unique
•  Tester localement avant de publier
•  Garder le dépôt propre et bien structuré


## 📘 Référence rapide

| Action                        | Commande / Interface         |
|------------------------------|------------------------------|
| Mise à jour du code          | `./update_git.sh`            |
| Redémarrer Home Assistant    | `ha core restart`            |
| Logs Home Assistant          | `ha core logs`               |
| Réinstaller via HACS         | Interface HACS               |
| Publication de release       | Automatique via GitHub Actions |