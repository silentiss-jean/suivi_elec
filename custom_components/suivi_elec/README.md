# 🔌 Suivi Élec — Intégration Home Assistant

Suivi Élec est une intégration personnalisée pour Home Assistant permettant de suivre la consommation énergétique, estimer les coûts, et générer des entités dynamiques à partir des capteurs disponibles.

---

## 🚀 Installation via HACS

### 1. Ajouter le dépôt personnalisé

1. Ouvrez Home Assistant à `http://homeassistant.local:8123`
2. Allez dans **HACS > Intégrations > ⋮ > Dépôts personnalisés**
3. Ajoutez ce dépôt :
https://github.com/silentiss-jean/suivi_elec.git
4. Type : **Intégration**
5. Cliquez sur **Ajouter**

---

### 2. Télécharger l’intégration

1. Allez dans **HACS > Intégrations**
2. Cliquez sur **+ Explorer et ajouter des intégrations**
3. Recherchez **Suivi Élec**
4. Cliquez sur **Télécharger**
5. Laissez les valeurs par défaut et validez

📌 À la fin du téléchargement, une alerte “1 Correction” apparaîtra dans **Paramètres > 1 Correction**  
Cliquez sur **Configurer l’intégration** pour lancer le formulaire de configuration

---

### 3. Configuration via l’interface graphique

L’intégration se configure via un formulaire simple :

- **URL de l’instance Home Assistant**  
Exemple : `http://homeassistant.local:8123` ou `https://monha.duckdns.org`

- **Jeton d’accès long-lived**  
À générer depuis votre profil utilisateur Home Assistant (`/profile`)

- **Instance locale ou distante** *(case à cocher)*  
Permet d’identifier visuellement les entités comme locales ou distantes

📌 Aucun paramètre ne doit être ajouté dans le fichier `configuration.yaml`.

---

## 🧠 Mode local vs distant

Ce paramètre ne modifie pas le fonctionnement technique, mais il permet :

- D’ajouter un tag `[Local]` ou `[Distant]` dans le `friendly_name` des entités
- De filtrer les entités dans les dashboards
- De suivre l’état global via le capteur `sensor.suivi_elec_status`

### Exemple :
```yaml
sensor.suivi_elec_status:
state: "local | 3 entités"
attributes:
 mode: "local"
 entites_actives:
   - sensor.suivi_elec_conso_jour
   - sensor.suivi_elec_tarif_hp
   - sensor.suivi_elec_tarif_hc
 source: "http://homeassistant.local:8123"
 last_update: "2025-09-12T21:49:00"
⚙️ Options système

Accessible via Paramètres > Intégrations > ⋮ > Options système
🧪 Vérifications post-installation

1.  Données stockées
  ⁠◦  Allez dans Développement > Intégrations > Détails
  ⁠◦  Vérifiez que entry.data contient :
      •  base_url
    •  ha_token
    •  is_local
2.  Entités créées
  ⁠◦  Allez dans Développement > États
  ⁠◦  Recherchez les entités activées
  ⁠◦  Vérifiez les attributs (friendly_name, source, unit_of_measurement)
3.  Capteur de statut
  ⁠◦  Recherchez : sensor.suivi_elec_status
  ⁠◦  Vérifiez :
      •  state → "local | 3 entités"
    •  attributes → mode, source, entites_actives, last_update
🚫 À ne pas faire

Ne pas ajouter de section suivi_elec: dans le fichier configuration.yaml.  
Cela déclenchera une alerte dans Home Assistant, car l’intégration ne lit pas ce fichier.
🛠️ Désinstallation propre

Utilisez le script uninstall_suivi_elec.sh pour supprimer proprement les fichiers générés.  
Consultez docs/uninstall_validation.txt pour vérifier que la suppression est complète.
