#!/bin/bash

NEW_TAG=$(./version_manager.sh)

TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
MANIFEST="custom_components/suivi_elec/manifest.json"

sed -i "s/\"version\": \".*\"/\"version\": \"${NEW_TAG#v}\"/" "$MANIFEST"

CHANGES=$(git status --porcelain)
if [ -z "$CHANGES" ]; then
  echo "⚠️ Aucun changement détecté. Rien à publier."
  exit 0
fi

git add .
git commit -m "📦 Release stable $NEW_TAG — horodaté $TIMESTAMP"
git tag -a "$NEW_TAG" -m "🔖 Version stable générée par release_stable.sh ($TIMESTAMP)"
git push origin dev
git push origin "$NEW_TAG"

echo ""
echo "✅ Version stable $NEW_TAG publiée avec succès"
