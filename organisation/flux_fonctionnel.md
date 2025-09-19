# Flux fonctionnel de l’intégration Suivi Élec

## 📈 Diagramme du flux fonctionnel

```mermaid
graph TD
  A[.env] --> B[env_loader.py]
  B --> C[api_client.py]
  C --> D[get_energy_entities]
  D --> E[detect_async.py]
  E --> F[calculateur.py]
  E --> G[historique.py]
  E --> H[tarif_loader.py]
  E --> I[cout_estime.json]
  I --> J[export_csv.py]
  E --> K[config.py]
  K --> L[settings.yaml]
  E --> M[groupes_capteurs_energy.py]
  M --> N[generator.py]
  N --> O[suivi_elec.yaml]
  N --> P[lovelace_conso.yaml]
  N --> Q[lovelace_history_conso.yaml]
  R[config_flow.py] --> S[options_flow.py]
  T[services.yaml] --> E

🔄 Description du flux

• config_flow.py permet à l’utilisateur de configurer l’intégration via l’interface Home Assistant  
• options_flow.py permet de modifier les paramètres après installation  
• .env est chargé par env_loader.py pour récupérer les variables sensibles (HA_URL, HA_TOKEN)  
• api_client.py teste la connexion à Home Assistant et récupère les entités énergétiques  
• detect_async.py est appelé automatiquement à l’installation pour orchestrer :

•  la détection
•  le calcul des coûts
•  la mise à jour de l’historique
•  la sauvegarde des résultats  
calccalculateur.pyme les coûts à partir des entités et des tarifs  
histhistorique.pyà jour le fichier `histhistorique_cout.json
taritarif_loader.pyge les tarifs depuis `taritarif.json
es résultats sont sauvegardés dans `coutcout_estime.json
confconfig.pysettsettings.yamlnissent les paramètres globaux  
grougroupes_capteurs_energy.pyinit les groupes utilisés pour la génération  
genegenerator.pyère les fichiers YAML (package, cartes Lovelace)  
servservices.yamlet de relancer manuellement le flux via `genegenerate_suivi_elec
expoexport_csv.pysforme les résultats en CSV pour exploitation externe

## 🧠 Synthèse des rôles

### 🔄 Scripts intégrés (automatiques)

| Fichier              | Rôle principal                                                                 |
|----------------------|--------------------------------------------------------------------------------|
| `detect_async.py`    | Détection automatique à l’installation via `async_setup_entry`                |
| `config_flow.py`     | Configuration initiale via l’interface Home Assistant                         |
| `options_flow.py`    | Modification des paramètres après installation                                |
| `services.yaml`      | Déclenchement manuel du flux via `generate_suivi_elec`                        |

### 🛠️ Scripts manuels (maintenance ou génération)

| Fichier                    | Rôle principal                                                          |
|----------------------------|-------------------------------------------------------------------------|
| `detect.py`                | Détection manuelle (hors cycle Home Assistant)                          |
| `generator.py`             | Génération des fichiers YAML et cartes Lovelace                         |
| `launcher.py`              | Chargement des groupes et affichage des capteurs                        |
| `generateur_entities.py`   | Simulation d’entités et création d’un capteur de statut                 |
| `export_csv.py`            | Export des résultats en CSV                                             |

### ⚙️ Fichiers de configuration

| Fichier                    | Rôle principal                                                          |
|----------------------------|-------------------------------------------------------------------------|
| `settings.yaml`            | Paramètres globaux (URL, token, regroupement, noms personnalisés)       |
| `config.py`                | Charge les paramètres depuis `settings.yaml`                            |
| `groupes_capteurs_energy.py` | Définition statique des groupes de capteurs énergétiques             |

