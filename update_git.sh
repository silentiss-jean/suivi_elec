#!/bin/bash

NEW_TAG=$(./version_manager.sh dev)
if [ -z "$NEW_TAG" ]; then
  echo "❌ Erreur : aucun tag généré. Abandon."
  exit 1
fi

echo "📦 Commit + tag : $NEW_TAG"

git add .
git commit -m "Auto release $NEW_TAG"
git tag -a "$NEW_TAG" -m "Auto release $NEW_TAG"
git push origin dev
git push origin "$NEW_TAG"

# Met à jour manifest.json
sed -i "s/\"version\": \".*\"/\"version\": \"${NEW_TAG#v}\"/" custom_components/suivi_elec/manifest.json
