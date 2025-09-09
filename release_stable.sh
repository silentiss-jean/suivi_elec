#!/bin/bash

NEW_TAG=$(./version_manager.sh)

echo "📦 Version stable : $NEW_TAG"

git add .
git commit -m "🔒 Version stable : $NEW_TAG"
git tag -a "$NEW_TAG" -m "Version stable : $NEW_TAG"
git push origin dev
git push origin "$NEW_TAG"

# Met à jour manifest.json
sed -i "s/\"version\": \".*\"/\"version\": \"${NEW_TAG#v}\"/" custom_components/suivi_elec/manifest.json
