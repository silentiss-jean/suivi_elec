# 🧩 Index des modules Python — Suivi Élec

Ce fichier centralise la documentation des modules internes utilisés par l’intégration Suivi Élec. Chaque module est documenté séparément dans le dossier `docs/`.

---

## 🔧 Modules principaux

| Module | Description | Documentation |
|--------|-------------|----------------|
| `api_client.py` | Connexion à l’API Home Assistant et récupération des entités | [📄 api_client.md](api_client.md) |
| `tarif_loader.py` | Chargement des tarifs depuis un fichier JSON | [📄 tarif_loader.md](tarif_loader.md) |
| `calculateur.py` | Calcul du coût estimé par entité | [📄 calculateur.md](calculateur.md) |
| `historique.py` | Mise à jour du fichier historique des coûts | [📄 historique.md](historique.md) |

---

## 📚 Autres fichiers utiles

- `config_flow.py` → Voir [📄 config_flow_modes.md](config_flow_modes.md)
- `detect.py` → Intégré dans le flux principal, dépend des modules ci-dessus
- `generateur_entities.py` → Génère les entités et le capteur de statut

---

## 🛠️ Structure recommandée

Tous les modules sont placés dans :
custom_components/suivi_elec/helpers/
Les fichiers de données sont dans :
custom_components/suivi_elec/data/
---

## 📌 À venir

- Ajout de tests unitaires pour chaque module
- Validation des formats JSON
- Intégration dans le script de synchronisation HACS
