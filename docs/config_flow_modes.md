# ⚙️ Configuration multi-mode — `config_flow.py`

## 🎯 Objectif

Permettre à l'utilisateur de choisir entre :

- 🏠 Mode **local** : instance Home Assistant locale (`http://homeassistant.local:8123`)
- ☁️ Mode **cloud** : instance distante via API (ex: EDF) avec token

---

## 🧩 Étapes dans le `config_flow`

1. L'utilisateur choisit le mode (`local` ou `cloud`)
2. Le formulaire s'adapte :
   - **Local** → URL locale + nom utilisateur
   - **Cloud** → URL distante + clé API
3. Le mode est stocké dans `entry.data["mode"]` pour usage ultérieur

---

## 🛠️ Exemple de données stockées

```json
{
  "mode": "cloud",
  "base_url": "https://api.edf.fr",
  "api_token": "abc123"
}
ou
{
  "mode": "local",
  "base_url": "http://homeassistant.local:8123",
  "nom_utilisateur": "admin"
}
🔁 Utilisation dans `__init__.py`

Le mode est utilisé pour :

•  Adapter les friendly_name des entités ([Local] ou [Cloud])
•  Ajouter un attribut source avec l’URL utilisée
•  Permettre des comportements différents selon le contexte
📁 Fichiers concernés

•  custom_components/suivi_elec/config_flow.py
•  custom_components/suivi_elec/__init__.py
•  docs/config_flow_modes.md (ce fichier)
---

---

## 🧠 Étape suivante : ajouter `sensor.suivi_elec_status`

Je vais maintenant te générer le code à ajouter dans `__init__.py` pour créer dynamiquement une entité `sensor.suivi_elec_status` qui affiche :

- Le mode actif (`local` ou `cloud`)
- Le nombre d’entités activées

---

## 🛠️ Commande shell pour mettre à jour `__init__.py`

```bash
cat >> /config/suivi_elec/custom_components/suivi_elec/__init__.py << 'EOF'

    # 🧠 Ajout du sensor de statut
    hass.states.async_set("sensor.suivi_elec_status", f"{mode} | {len(entites_actives)} entités", {
        "friendly_name": "Suivi Élec — Statut",
        "mode": mode,
        "entites_actives": len(entites_actives),
        "source": base_url
    })

🧪 Résultat attendu dans HA

Dans Développement > États, tu verras :

sensor.suivi_elec_status
→ state: cloud | 3 entités
→ attributes:
   - friendly_name: Suivi Élec — Statut
   - mode: cloud
   - entites_actives: 3
   - source: https://api.edf.fr
