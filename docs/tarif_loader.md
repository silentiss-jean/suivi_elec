# 📦 Module `helpers/tarif_loader.py`

Ce module permet de charger les tarifs d’électricité depuis un fichier JSON. Il est utilisé par `detect.py` pour calculer les coûts estimés.

---

## 🔧 Fonction principale

### `load_tarifs(path)`

Charge et valide le fichier de tarifs.

- 📥 Paramètre : chemin vers le fichier `.json`
- 📤 Retour : dictionnaire des tarifs ou `None` en cas d’erreur
- ❌ Affiche les erreurs en console si le fichier est absent ou mal formé

---

## 📄 Format attendu

```json
{
  "kwh": 0.174,
  "hp": 0.2068,
  "hc": 0.1565
}
•  kwh : tarif par défaut
•  hp : Heures Pleines
•  hc : Heures Creuses
🛡️ Sécurité

Le module ne fait que lire un fichier local. Il ne dépend d’aucune API externe et ne modifie aucune donnée.

📚 Utilisation typique

Dans detect.py :
from helpers.tarif_loader import load_tarifs

tarifs = load_tarifs("custom_components/suivi_elec/data/tarif.json")
🧪 À tester

•  Fichier bien formé → retourne un dict
•  Fichier absent → affiche une erreur et retourne None
•  Fichier mal formé → affiche une erreur et retourne None
•  Format non dict → affiche une erreur
