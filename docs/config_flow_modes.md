# ⚙️ Configuration — `config_flow.py`

Ce module gère le formulaire de configuration initial de l’intégration Suivi Élec dans Home Assistant. Il permet de définir le mode de connexion, le type de contrat, les tarifs, et l’abonnement.

---

## 🧩 Paramètres disponibles

| Clé | Description |
|-----|-------------|
| `name` | Nom de l’intégration |
| `mode` | `local` ou `remote` |
| `token` | Jeton d’accès long-lived |
| `url` | URL de l’instance Home Assistant (mode remote) |
| `type_contrat` | `prix_unique` ou `heures_pleines_creuses` |
| `prix_ht`, `prix_ttc` | Tarifs pour contrat unique |
| `prix_ht_hp`, `prix_ttc_hp` | Tarifs Heures Pleines |
| `prix_ht_hc`, `prix_ttc_hc` | Tarifs Heures Creuses |
| `heure_debut_hp`, `heure_fin_hp` | Plage horaire HP |
| `abonnement_annuel` | Montant annuel de l’abonnement |

---

## 🔐 Validation intégrée

- Jeton requis et longueur minimale
- URL obligatoire en mode `remote`
- Conversion automatique des champs numériques (`vol.Coerce(float)`)

---

## 🧠 Logique de tarification

- Si `type_contrat = prix_unique` → utilise `prix_ht` et `prix_ttc`
- Si `type_contrat = heures_pleines_creuses` → détection HP/HC selon l’heure
- Si `prix_ttc` est vide → calculé automatiquement via `prix_ht * 1.2`

---

## 🧾 Exemple de configuration

```json
{
  "name": "Suivi Électricité",
  "mode": "local",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "type_contrat": "heures_pleines_creuses",
  "prix_ht_hp": 0.2068,
  "prix_ttc_hp": 0.2482,
  "prix_ht_hc": 0.1565,
  "prix_ttc_hc": 0.1878,
  "heure_debut_hp": "06:00",
  "heure_fin_hp": "22:00",
  "abonnement_annuel": 120.0
}

🧪 À tester

•  Mode remote sans URL → erreur url_requise
•  Jeton vide ou trop court → erreur token_invalide
•  Contrat prix_unique → champs HP/HC ignorés
•  Contrat heures_pleines_creuses → détection horaire correcte
•  Abonnement vide → fallback sur 0

📚 Options avancées

Voir le fichier options_flow.py pour la gestion des options post-installation.
