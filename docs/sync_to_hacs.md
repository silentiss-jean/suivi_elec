# 🔄 Script `sync_to_hacs.sh`

## 🎯 Objectif

Ce script permet de synchroniser rapidement le code de développement de l'intégration `suivi_elec` vers le dossier utilisé par Home Assistant Core (`/config/custom_components/suivi_elec`), puis de redémarrer Home Assistant et d'afficher les logs liés à l'intégration.

---

## 📦 Fonctionnalités

- 🧼 Nettoyage du dossier HACS
- 📁 Copie des fichiers depuis le dossier de développement
- 🔁 Redémarrage de Home Assistant Core
- 🔍 Analyse des logs contenant `suivi_elec`

---

## 📁 Emplacement recommandé

Place ce script dans :
/config/suivi_elec/sync_to_hacs.sh
---

## 🚀 Utilisation

```bash
bash /config/suivi_elec/sync_to_hacs.sh
🛠️ Exemple de contenu du script
#!/bin/bash

echo "🧼 Nettoyage du dossier HACS..."
rm -rf /config/custom_components/suivi_elec/*

echo "📦 Copie des fichiers depuis le dossier de dev..."
cp -r /config/suivi_elec/custom_components/suivi_elec/* /config/custom_components/suivi_elec/

echo "🔁 Redémarrage de Home Assistant Core..."
ha core restart

echo "⏳ Attente du redémarrage..."
sleep 10

echo "🔍 Analyse des logs pour 'suivi_elec'..."
ha core logs | grep -i suivi_elec | tail -n 20

echo "✅ Synchronisation terminée. Vérifie ci-dessus s’il y a des erreurs."
