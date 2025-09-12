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
