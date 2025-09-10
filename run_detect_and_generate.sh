#!/bin/bash

echo "🔍 Détection des entités énergétiques..."
python3 custom_components/suivi_elec/helpers/detect.py

echo "🧪 Vérification du format JSON..."
python3 custom_components/suivi_elec/helpers/test_detect_format.py

echo "⚙️ Génération des fichiers de configuration..."
python3 custom_components/suivi_elec/generator.py

echo "✅ Processus terminé."
