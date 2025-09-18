# Scripts inutilisés ou à archiver

Ce fichier recense les modules présents dans `helpers/` qui sont redondants, obsolètes ou non intégrés dans le flux principal.

---

## ❌ À renommer en `inutil_*.py`

| Fichier                  | Problème identifié                                 | Remarques                  |
|--------------------------|----------------------------------------------------|----------------------------|
| `check_env.py`           | Redondant avec `env_loader.py`                    | Test manuel, non intégré   |
| `check_token_direct.py`  | Token en clair, test manuel                       | Risque de sécurité         |
| `config_flow_toremove.py`| Flow UI non actif ou désactivé                    | À confirmer dans `manifest.json` |

---

## 🟡 À confirmer / en attente d’intégration

| Fichier            | Rôle potentiel                              | Action recommandée          |
|--------------------|---------------------------------------------|------------------------------|
| `loader.py`        | Chargement dynamique de groupes             | Vérifier usage réel          |
| `regroupement.py`  | Génère fichiers `groupes_capteurs_*.py`     | Intégrer ou archiver         |
| `export_csv.py`    | Export manuel des résultats                 | Automatiser ou archiver      |

---

## 🧼 Recommandations

- Renommer les fichiers inutilisés avec le préfixe `inutil_` pour les exclure du flux principal
- Ajouter un `.gitignore` si certains fichiers ne doivent pas être versionnés
- Documenter dans `README.md` que ces fichiers sont conservés à des fins de test ou d’archivage

## 🔄 Mise à jour - Septembre 2025

- Le module `groupes_capteurs_energy.py` est désormais utilisé par `generation.py` → à retirer de la liste des fichiers non utilisés
- La fonction `get_energy_entities()` est maintenant testée → ne plus considérer comme non couverte
