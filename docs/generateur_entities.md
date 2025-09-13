# ⚙️ Générateur d'entités — `generateur_entities.py`

Ce script permet de simuler des entités énergétiques et de créer un capteur de statut global pour l’intégration Suivi Élec. Il est utile pour les tests locaux, les démonstrations ou le développement hors production.

---

## 🔧 Fonctions principales

### `charger_entry_data(path)`
Charge les paramètres d’entrée (`entry_data.json`) ou retourne des valeurs par défaut (`local`, `base_url`).

### `generer_entites(n, mode, base_url)`
Génère `n` entités simulées avec :
- `entity_id` unique
- `state` aléatoire entre 0.5 et 5.0 kWh
- Tag tarifaire aléatoire : `hp`, `hc`, ou standard
- Attributs enrichis : `friendly_name`, `source`, `unit_of_measurement`

### `generer_status(entites, mode, base_url)`
Crée le capteur `sensor.suivi_elec_status` avec :
- `state` : `"local | 10 entités"`
- `attributes` : `mode`, `source`, `entites_actives`, `last_update`

---

## 📄 Fichiers générés

| Fichier | Contenu |
|--------|---------|
| `capteurs_detectes.json` | Liste des entités simulées |
| `status_sensor.json` | Capteur de statut global |
| `entry_data.json` | Paramètres d’entrée (mode, base_url) |

---

## 🧪 À tester

- Fichier `entry_data.json` absent → fallback sur `local`
- Génération de 10 entités → fichier bien formé
- Capteur de statut → contient `mode`, `source`, `last_update`
- Tags tarifaires → bien répartis entre `hp`, `hc`, et standard

---

## 📚 Utilisation

```bash
python3 custom_components/suivi_elec/helpers/generateur_entities.py
cat > docs/generateur_yaml.md << 'EOF'
# 🧾 Générateur YAML & Lovelace — `generateur_yaml.py`

Ce script génère automatiquement :
- Un fichier YAML pour Home Assistant (`suivi_elec.yaml`)
- Une carte Lovelace par pièce (`lovelace_conso.yaml`)
- Une carte historique (`lovelace_history_conso.yaml`)

Il prend en charge :
- Le mode `energy` (consommation) ou `power` (puissance)
- Les cycles `jour`, `semaine`, `mois`, `annee`
- Le calcul des coûts avec abonnement annuel
- Les groupes de capteurs par pièce

---

## 🔧 Fonctions principales

### `generate_yaml_config(capteurs, config_data)`
Crée les entités `sensor.energy_*`, les utility meters, et les capteurs de coût avec abonnement.

### `generate_lovelace_grid(groupes)`
Génère une carte Lovelace par pièce avec les entités de consommation et coût.

### `generate_history_card(groupes)`
Crée une carte `history-explorer` avec les coûts ou puissances par pièce.

### `run_all(config_data)`
Exécute toutes les fonctions et écrit les fichiers dans `data/`.

---

## 📄 Fichiers générés

| Fichier | Description |
|--------|-------------|
| `suivi_elec.yaml` | Package HA avec sensors, utility meters, coût |
| `lovelace_conso.yaml` | Carte Lovelace par pièce |
| `lovelace_history_conso.yaml` | Carte historique (custom:history-explorer) |

---

## 🧪 À tester

- Mode `energy` → capteurs `sensor.energy_*` + coût
- Mode `power` → capteurs bruts + puissance
- Abonnement activé → coût ajusté
- Groupes bien définis → cartes par pièce cohérentes

---

## 📚 Exemple d’exécution

```bash
python3 custom_components/suivi_elec/helpers/generateur_yaml.py
📌 Remarques

•  Le fichier groupes_capteurs_energy.py doit contenir un dictionnaire groupes = {...}
•  Le mode peut être changé en haut du script (mode = "power")

