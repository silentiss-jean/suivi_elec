#!/bin/bash

VENV_DIR=".venv"

echo "🐍 Chargement de l'environnement virtuel Python..."

# Créer le venv s'il n'existe pas
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Aucun venv trouvé, création en cours..."
    python3 -m venv "$VENV_DIR"
    echo "✅ Environnement virtuel créé dans $VENV_DIR"
fi

# Activer le venv
source "$VENV_DIR/bin/activate"
echo "🚀 Environnement virtuel activé."

# Installer les dépendances si requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "📚 Installation des dépendances..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dépendances installées."
else
    echo "📁 Aucun fichier requirements.txt trouvé, installation ignorée."
fi
