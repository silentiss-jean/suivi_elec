# ⚙️ Options post-installation — `options_flow.py`

Ce module permet à l’utilisateur de modifier les paramètres de l’intégration Suivi Élec **après installation**, via l’interface Home Assistant (⋮ > Options). Il reprend les mêmes champs que le `config_flow.py`, avec les valeurs déjà enregistrées.

---

## 🧩 Paramètres modifiables

| Clé | Description |
|-----|-------------|
| `mode` | `local` ou `remote` |
| `url` | URL de l’instance Home Assistant |
| `type_contrat` | `prix_unique` ou `heures_pleines_creuses` |
| `prix_ht`, `prix_ttc` | Tarifs pour contrat unique |
| `prix_ht_hp`, `prix_ttc_hp` | Tarifs Heures Pleines |
| `prix_ht_hc`, `prix_ttc_hc` | Tarifs Heures Creuses |
| `heure_debut_hp`, `heure_fin_hp` | Plage horaire HP |
| `abonnement_annuel` | Montant annuel de l’abonnement |

---

## 🔄 Fonctionnement

- Les valeurs actuelles sont pré-remplies depuis `config_entry.options` ou `config_entry.data`
- L’utilisateur peut les modifier sans réinstaller l’intégration
- Les champs numériques sont convertis automatiquement (`vol.Coerce(float)`)

---

## 🧾 Exemple d’édition

L’utilisateur peut :
- Passer du mode `local` à `remote`
- Corriger une erreur de tarif
- Modifier la plage horaire HP
- Activer ou désactiver l’abonnement

---

## 🧪 À tester

- Modification du mode → prise en compte dans le capteur `suivi_elec_status`
- Changement de tarif → impact sur le calcul dans `calculateur.py`
- Plage HP chevauchante → test avec `est_hp()`
- Abonnement modifié → test avec `inclure_abonnement = True`

---

## 📚 Liens utiles

- [Configuration initiale](config_flow_modes.md)
- [Calcul des coûts](calculateur.md)
- [Détection HP/HC](calculateur_hp_hc.md)
