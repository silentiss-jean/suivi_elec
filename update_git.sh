#!/bin/bash

NEW_TAG=$(./version_manager.sh)

if [ -z "$NEW_TAG" ]; then
  echo "❌ Aucun tag généré. Abandon."
  exit 1
fi

# Horodatage pour le commit
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")

echo "📦 Commit + tag : $NEW_TAG ($TIMESTAMP)"

# Commit + tag
git add .
git commit -m "Auto release $NEW_TAG — horodaté $TIMESTAMP"
git tag -a "$NEW_TAG" -m "Auto release $NEW_TAG — horodaté $TIMESTAMP"
git push origin dev
git push origin "$NEW_TAG"

# Met à jour manifest.json
sed -i "s/\"version\": \".*\"/\"version\": \"${NEW_TAG#v}\"/" custom_components/suivi_elec/manifest.json
