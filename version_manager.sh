#!/bin/bash

# Récupère le dernier tag SemVer (stable ou dev)
LAST_TAG=$(git tag --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+' | tail -n 1)

# Si aucun tag, on commence à v1.0.0
if [ -z "$LAST_TAG" ]; then
  BASE_VERSION="v1.0.0"
else
  BASE_VERSION="$LAST_TAG"
fi

# Génère un timestamp
TIMESTAMP=$(date +"%Y%m%d.%H%M")

# Si mode dev, ajoute suffixe
if [ "$1" == "dev" ]; then
  NEW_TAG="${BASE_VERSION}-dev.${TIMESTAMP}"
else
  # Incrémente le patch
  MAJOR=$(echo "$BASE_VERSION" | cut -d. -f1 | tr -d 'v')
  MINOR=$(echo "$BASE_VERSION" | cut -d. -f2)
  PATCH=$(echo "$BASE_VERSION" | cut -d. -f3)
  NEXT=$((10#$PATCH + 1))
  NEW_TAG="v${MAJOR}.${MINOR}.${NEXT}"
fi

echo "$NEW_TAG"
