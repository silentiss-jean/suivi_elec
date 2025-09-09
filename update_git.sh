#!/bin/bash

NEW_TAG=$(./version_manager.sh)

TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
MANIFEST="custom_components/suivi_elec/manifest.json"

# 📦 Met à jour manifest.json
sed -i "s/\"version\": \".*\"/\"version\": \"${NEW_TAG#v}\"/" "$MANIFEST"

# 🔍 Vérifie les changements
CHANGES=$(git status --porcelain)
if [ -z "$CHANGES" ]; then
  echo "⚠️ Aucun changement détecté. Rien à publier."
  exit 0
fi

# ✅ Commit + tag
git add .
git commit -m "🔧 Auto update $NEW_TAG — horodaté $TIMESTAMP"
git tag -a "$NEW_TAG" -m "🧪 Version auto générée par update_git.sh ($TIMESTAMP)"
git push origin dev
git push origin "$NEW_TAG"

echo ""
echo "✅ Version auto $NEW_TAG publiée avec succès"
