# Documentation des scripts `helpers/`

Ce fichier décrit le rôle de chaque script présent dans `custom_components/suivi_elec/helpers`.

---

## ✅ Scripts actifs

| Fichier                | Rôle principal                                      | Utilisé dans             |
|------------------------|-----------------------------------------------------|---------------------------|
| `api_client.py`        | Connexion à l’API Home Assistant                    | `detect.py`               |
| `calculateur.py`       | Calcul du coût énergétique                          | `detect.py`               |
| `env_loader.py`        | Chargement des variables d’environnement            | `detect.py`               |
| `historique.py`        | Mise à jour de l’historique de consommation         | `detect.py`               |
| `tarif_loader.py`      | Chargement et validation des tarifs                 | `detect.py`               |
| `detect_utils.py`      | Détection du mode, des entités, du contrat          | `config_flow`, `setup`    |
| `entity_selector.py`   | Comparaison entre entités existantes et potentielles| `generation`, `detect`    |
| `generation.py`        | Génération YAML + Lovelace + historique             | Script manuel             |
| `generateur_entites.py`| Simulation d’entités et capteur de statut          | Script manuel             |
| `mise_a_jour_entites.py`| Synchronisation des entités de suivi               | Script manuel             |

---

## 🟡 Scripts à confirmer / en attente

| Fichier                | Rôle principal                                      | Statut                   |
|------------------------|-----------------------------------------------------|---------------------------|
| `loader.py`            | Chargement dynamique de groupes                     | À confirmer               |
| `regroupement.py`      | Regroupement des capteurs par pièce                 | À confirmer               |
| `export_csv.py`        | Export des résultats vers CSV                       | Script manuel             |

---

## ❌ Scripts obsolètes ou redondants

| Fichier                    | Problème identifié                               | Action recommandée        |
|----------------------------|--------------------------------------------------|----------------------------|
| `check_env.py`             | Redondant avec `env_loader.py`                  | Renommer en `inutil_*.py` |
| `check_token_direct.py`    | Token en clair, test manuel                     | Supprimer ou archiver     |
| `config_flow_toremove.py`  | Flow UI non intégré ou désactivé                | Renommer ou archiver      |

---

## 🔄 Mise à jour recommandée

- Ajouter ce fichier dans ton dépôt Git pour qu’il soit visible dès le clonage
- Mettre à jour ton `README.md` pour pointer vers `organisation/structure.md`
- Ajouter un fichier `flux_fonctionnel.md` pour visualiser les interactions entre modules

---
