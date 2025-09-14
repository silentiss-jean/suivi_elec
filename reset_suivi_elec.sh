#!/bin/bash

echo "🧹 Nettoyage complet de l'intégration Suivi Élec..."

# Supprimer les caches Python
echo "🧽 Suppression des fichiers __pycache__ et *.pyc..."
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Supprimer les fichiers générés
echo "🗑️ Suppression des fichiers JSON et YAML générés..."
rm -f custom_components/suivi_elec/data/*.json
rm -f custom_components/suivi_elec/data/*.yaml
rm -rf custom_components/suivi_elec/data/generated/

# Nettoyage Git (optionnel)
read -p "⚠️ Souhaitez-vous supprimer tous les fichiers non suivis par Git ? (y/N): " confirm
if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
    echo "🧨 Exécution de git clean -fdx..."
    git clean -fdx
else
    echo "🚫 Nettoyage Git annulé."
fi

echo "✅ Nettoyage terminé. Tu peux relancer l'intégration proprement."
