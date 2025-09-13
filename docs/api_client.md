# 🌐 Module `helpers/api_client.py`

Ce module permet d’interagir avec l’API REST de Home Assistant. Il est utilisé par `detect.py` pour tester la connexion et récupérer les entités énergétiques.

---

## 🔧 Fonctions disponibles

### `test_api_connection(base_url, token)`

Teste la connexion à l’API Home Assistant.

- 🔐 Utilise le jeton d’accès long-lived (`Authorization: Bearer`)
- 📍 URL cible : `GET <base_url>/api/`
- ✅ Retourne `True` si le code HTTP est 200
- ❌ Retourne `False` en cas d’erreur ou d’échec

---

### `get_energy_entities(base_url, token)`

Récupère toutes les entités, puis filtre celles liées à l’énergie.

- 📍 URL cible : `GET <base_url>/api/states`
- 🔍 Filtrage :
  - Domaine : `sensor.`
  - Unité ou état contenant `kwh`
- 📦 Retourne une liste d’entités :
```json
{
  "entity_id": "sensor.suivi_elec_conso_jour",
  "state": "12.5",
  "name": "Consommation Jour",
  "unit": "kWh"
}
🛡️ Sécurité

Ce module utilise uniquement des appels en lecture (GET).  
Le jeton utilisé doit être généré depuis /profile et avoir les droits de lecture.

📚 Utilisation typique
from helpers.api_client import test_api_connection, get_energy_entities

if test_api_connection(HA_URL, HA_TOKEN):
    entities = get_energy_entities(HA_URL, HA_TOKEN)

🧪 À tester

•  Connexion à une instance locale et distante
•  Filtrage correct des entités énergétiques
•  Gestion des erreurs réseau ou jeton invalide
