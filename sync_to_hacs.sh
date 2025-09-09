#!/bin/bash
echo "🧼 Nettoyage du dossier HACS..."
rm -rf /config/custom_components/suivi_elec/*
echo "📦 Copie des fichiers depuis le dossier de dev..."
cp -r /config/suivi_elec/* /config/custom_components/suivi_elec/
echo "✅ Synchronisation terminée."
