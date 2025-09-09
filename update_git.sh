#!/bin/bash

# 🔧 Génère un tag de dev
NEW_TAG=$(./version_manager.sh dev)

if [ -z "$NEW_TAG" ]; then
  echo "❌ Aucun tag généré. Abandon."
  exit 1
fi

# 🔒 Vérifie que le tag n'existe pas déjà
if git rev-parse "$NEW_TAG" >/dev/null 2>&1; then
  echo "❌ Le tag $NEW_TAG existe déjà. Abandon."
  exit 1
fi

# 🕒 Horodatage pour le commit
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")

# 🔒 Vérifie qu’il y a des fichiers modifiés ou ajoutés
CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
  echo "⚠️ Aucun changement détecté. Rien à publier."
  exit 0
fi

# ✅ Commit + tag
git add .
git commit -m "🧪 Auto release $NEW_TAG — horodaté $TIMESTAMP"
git tag -a "$NEW_TAG" -m "🧪 Auto release $NEW_TAG — horodaté $TIMESTAMP"
git push origin dev
git push origin "$NEW_TAG"

echo ""
echo "✅ Version dev $NEW_TAG publiée avec succès"
echo "📁 Fichiers modifiés :"
echo "$CHANGES"
