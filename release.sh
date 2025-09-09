#!/bin/bash

# 🔍 Trouve le dernier tag SemVer pur
LAST_TAG=$(git tag --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | tail -n 1)

if [ -z "$LAST_TAG" ]; then
  MAJOR=0
  MINOR=9
  PATCH=0
else
  MAJOR=$(echo "$LAST_TAG" | cut -d. -f1 | tr -d 'v')
  MINOR=$(echo "$LAST_TAG" | cut -d. -f2)
  PATCH=$(echo "$LAST_TAG" | cut -d. -f3)
fi

# 🔁 Incrémente jusqu'à trouver un tag libre
while true; do
  PATCH=$((PATCH + 1))
  NEW_TAG="v${MAJOR}.${MINOR}.${PATCH}"
  if ! git rev-parse "$NEW_TAG" >/dev/null 2>&1; then
    break
  fi
done

# 🕒 Horodatage
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")

# 📦 Met à jour manifest.json
MANIFEST="custom_components/suivi_elec/manifest.json"
sed -i "s/\"version\": \".*\"/\"version\": \"${NEW_TAG#v}\"/" "$MANIFEST"

# 🔍 Vérifie les changements
CHANGES=$(git status --porcelain)
if [ -z "$CHANGES" ]; then
  echo "⚠️ Aucun changement détecté. Rien à publier."
  exit 0
fi

# ✅ Commit + tag
git add .
git commit -m "🚀 Release $NEW_TAG — horodaté $TIMESTAMP"
git tag -a "$NEW_TAG" -m "✅ Version compatible HACS générée par release.sh ($TIMESTAMP)"
git push origin dev
git push origin "$NEW_TAG"

echo ""
echo "✅ Version $NEW_TAG publiée avec succès et compatible HACS"
