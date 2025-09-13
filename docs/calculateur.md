# 🧮 Module `helpers/calculateur.py`

Ce module calcule le coût estimé d’une entité énergétique en fonction de sa consommation et du tarif applicable. Il est utilisé dans `detect.py`.

---

## 🔧 Fonction principale

### `calculer_cout(entity, tarifs)`

Calcule le coût estimé pour une entité.

- 📥 Paramètres :
  - `entity` : dictionnaire contenant `state`, `entity_id`, `attributes`
  - `tarifs` : dictionnaire des tarifs (`hp`, `hc`, `kwh`)
- 📤 Retour : dictionnaire avec les détails du calcul
- ❌ Retourne `None` si l’état est invalide ou une erreur survient

---

## 📄 Exemple d’entrée

```json
{
  "entity_id": "sensor.tarif_hp",
  "state": "15.2",
  "attributes": {
    "friendly_name": "Tarif HP"
  }
}

📄 Exemple de sortie
{
  "entity_id": "sensor.tarif_hp",
  "nom": "Tarif HP",
  "energie_kwh": 15.2,
  "prix_kwh": 0.2068,
  "mode_tarif": "heures pleines",
  "total_ht": 3.14,
  "total_ttc": 3.77
}
🧠 Logique de détection du tarif

•  Si entity_id contient "hc" → tarif hc → mode "heures creuses"
•  Si entity_id contient "hp" → tarif hp → mode "heures pleines"
•  Sinon → tarif kwh → mode "standard"

🧪 À tester

•  Entité avec état "unknown" ou "unavailable" → ignorée
•  Entité avec valeur numérique → calcul OK
•  Tarif manquant → fallback sur tarifs["kwh"]
•  Calcul HT + TVA (20%)
