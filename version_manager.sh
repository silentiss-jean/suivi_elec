#!/bin/bash

# Récupère le dernier tag SemVer pur
LAST_TAG=$(git tag --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | tail -n 1)

# Si aucun tag, on commence à v0.9.0
if [ -z "$LAST_TAG" ]; then
  MAJOR=0
  MINOR=9
  PATCH=0
else
  MAJOR=$(echo "$LAST_TAG" | cut -d. -f1 | tr -d 'v')
  MINOR=$(echo "$LAST_TAG" | cut -d. -f2)
  PATCH=$(echo "$LAST_TAG" | cut -d. -f3)
  PATCH=$((PATCH + 1))
fi

# Génère le nouveau tag
NEW_TAG="v${MAJOR}.${MINOR}.${PATCH}"

# Affiche le tag
echo "$NEW_TAG"
