# 📈 Module `helpers/historique.py`

Ce module permet de maintenir un historique des coûts et consommations énergétiques dans un fichier JSON. Il est utilisé par `detect.py` pour ajouter une entrée à chaque exécution.

---

## 🔧 Fonction principale

### `update_historique(filepath, total_ttc, total_kwh)`

Ajoute une nouvelle entrée dans le fichier historique.

- 📥 Paramètres :
  - `filepath` : chemin du fichier JSON à mettre à jour
  - `total_ttc` : coût total TTC calculé
  - `total_kwh` : énergie totale consommée en kWh
- 📤 Effet : ajoute une ligne avec la date du jour, le coût et la consommation

---

## 📄 Format du fichier historique

```json
[
  {
    "date": "2025-09-12",
    "total_ttc": 3.77,
    "total_kwh": 15.2
  },
  {
    "date": "2025-09-13",
    "total_ttc": 4.12,
    "total_kwh": 16.8
  }
]

🛡️ Sécurité

Le module écrase le fichier existant avec les nouvelles données.  
Il ne fait pas de backup automatique — à prévoir si besoin.

📚 Utilisation typique

Dans detect.py :
from helpers.historique import update_historique

update_historique("custom_components/suivi_elec/data/historique_cout.json", total_ttc, total_kwh)

🧪 À tester

•  Fichier existant → ajoute une ligne
•  Fichier absent → crée un nouveau fichier
•  Données corrompues → lève une exception
