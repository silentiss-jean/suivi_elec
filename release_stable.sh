#!/bin/bash

NEW_TAG=$(./version_manager.sh stable)

if [ -z "$NEW_TAG" ]; then
  echo "❌ Aucun tag généré. Abandon."
  exit 1
fi

if git rev-parse "$NEW_TAG" >/dev/null 2>&1; then
  echo "❌ Le tag $NEW_TAG existe déjà. Abandon."
  exit 1
fi

TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
MANIFEST="custom_components/suivi_elec/manifest.json"

sed -i "s/\"version\": \".*\"/\"version\": \"${NEW_TAG#v}\"/" "$MANIFEST"

if ! grep -q "\"version\": \"${NEW_TAG#v}\"" "$MANIFEST"; then
  echo "❌ manifest.json n'est pas à jour. Abandon."
  exit 1
fi

CHANGES=$(git status --porcelain)

if [ -z "$CHANGES" ]; then
  echo "⚠️ Aucun changement détecté. Rien à publier."
  exit 0
fi

git add .
git commit -m "🔖 Release stable $NEW_TAG — horodaté $TIMESTAMP"
git tag -a "$NEW_TAG" -m "🔖 Release stable $NEW_TAG — horodaté $TIMESTAMP"
git push origin dev
git push origin "$NEW_TAG"

echo ""
echo "✅ Release stable $NEW_TAG publiée avec succès"
echo "📁 Fichiers modifiés :"
echo "$CHANGES"
