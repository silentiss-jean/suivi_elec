#!/bin/bash

# 🔍 Récupère le dernier tag Git trié par version (en excluant les horodatés)
LAST_TAG=$(git tag --sort=-v:refname | grep -E '^v([0-9]+\.[0-9]+\.[0-9]+|[0-9]{8}(\.[0-9]+)?)$' | head -n 1)

echo "🔖 Dernier tag détecté : $LAST_TAG"

# 🧠 Si aucun tag, on commence à v1.0.0
if [ -z "$LAST_TAG" ]; then
  NEW_TAG="v1.0.0"
else
  RAW_TAG=${LAST_TAG#v}

  # Format date pur ou date.suffix
  if [[ "$RAW_TAG" =~ ^[0-9]{8}(\.[0-9]+)?$ ]]; then
    BASE=$(echo "$RAW_TAG" | cut -d. -f1)
    SUFFIX=$(echo "$RAW_TAG" | cut -d. -f2)

    if [ -z "$SUFFIX" ]; then
      NEW_TAG="v${BASE}.1"
    else
      NEXT=$((10#$SUFFIX + 1))
      NEW_TAG="v${BASE}.${NEXT}"
    fi

  # Format classique x.y.z
  elif [[ "$RAW_TAG" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    MAJOR=$(echo "$RAW_TAG" | cut -d. -f1)
    MINOR=$(echo "$RAW_TAG" | cut -d. -f2)
    PATCH=$(echo "$RAW_TAG" | cut -d. -f3)
    NEXT=$((10#$PATCH + 1))
    NEW_TAG="v${MAJOR}.${MINOR}.${NEXT}"
  else
    echo "⚠️ Format de tag inconnu : $LAST_TAG"
    exit 1
  fi
fi

echo "📦 Nouveau tag généré : $NEW_TAG"

# 🧼 Commit si nécessaire
if ! git diff --quiet; then
  git add .
  git commit -m "🔒 Version stable : $NEW_TAG"
else
  echo "ℹ️ Aucun changement à committer"
fi

# 🏷️ Création du tag
git tag -a "$NEW_TAG" -m "Version stable : $NEW_TAG"
git push origin dev
git push origin "$NEW_TAG"

echo "✅ Release poussée avec succès : $NEW_TAG"
