#!/bin/bash

# 🔧 Génère un nouveau tag SemVer pur
NEW_TAG=$(./version_manager.sh)

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

# 📦 Met à jour manifest.json
sed -i "s/\"version\": \".*\"/\"version\": \"${NEW_TAG#v}\"/" custom_components/suivi_elec/manifest.json

# 🔒 Vérifie que manifest.json est bien mis à jour
if ! grep -q "\"version\": \"${NEW_TAG#v}\"" custom_components/suivi_elec/manifest.json; then
  echo "❌ manifest.json n'est pas à jour. Abandon."
  exit 1
fi

# 🔒 Vérifie qu’il y a des modifications à committer
if git diff --quiet && git diff --cached --quiet; then
  echo "⚠️ Aucun changement détecté. Rien à publier."
  exit 0
fi

# ✅ Commit + tag
git add .
git commit -m "🔖 Release stable $NEW_TAG — horodaté $TIMESTAMP"
git tag -a "$NEW_TAG" -m "🔖 Release stable $NEW_TAG — horodaté $TIMESTAMP"
git push origin dev
git push origin "$NEW_TAG"

echo "✅ Release stable $NEW_TAG
