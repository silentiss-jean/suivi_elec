# 📚 Documentation Développement — `suivi_elec`

Bienvenue dans l’espace développeur de l’intégration `suivi_elec`. Ce dossier regroupe tous les outils, scripts et guides utiles pour tester, publier et maintenir ton intégration Home Assistant.

---

## 🛠️ Scripts de développement

| Script                  | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| [`release.sh`](release.sh)         | Génère un nouveau tag SemVer, met à jour le `manifest.json`, commit + push Git |
| [`sync_to_hacs.sh`](sync_to_hacs.sh) | Copie les fichiers de dev vers `/config/custom_components/`, redémarre HA et affiche les logs |
| [`sync.sh`](sync.sh)               | Variante simple pour synchroniser sans redémarrage ni logs |

---

## 📦 Fichiers de configuration

| Fichier                         | Rôle                                                                 |
|--------------------------------|----------------------------------------------------------------------|
| `manifest.json`                | Métadonnées de l’intégration (nom, version, dépendances, etc.)      |
| `config_flow.py`               | Interface utilisateur pour configurer l’intégration et ses options  |
| `const.py`                     | Constantes partagées (domain, clés, entités potentielles)           |
| `translations/fr.json`         | Traductions françaises pour l’interface Home Assistant               |

---

## 📁 Dossiers utiles

| Dossier                        | Contenu                                                              |
|-------------------------------|----------------------------------------------------------------------|
| `custom_components/suivi_elec/` | Code source de l’intégration                                         |
| `helpers/`                    | Modules utilitaires (API, calculs, historique, etc.)                 |
| `docs/`                       | Documentation technique et scripts liés au développement             |

---

## 🚀 Bonnes pratiques

- Utilise `sync_to_hacs.sh` pour tester rapidement tes modifications locales
- Lance `release.sh` uniquement quand tu es prêt à publier une version stable
- Documente chaque script ou module dans ce dossier pour faciliter la maintenance

---

## ✍️ À compléter

Tu peux ajouter ici :
- Un guide d’installation manuel
- Des exemples de configuration YAML
- Des captures d’écran Lovelace
