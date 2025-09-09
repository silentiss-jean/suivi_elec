#!/bin/bash

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

# 🔁 Boucle jusqu'à trouver un tag libre
while true; do
  PATCH=$((PATCH + 1))
  NEW_TAG="v${MAJOR}.${MINOR}.${PATCH}"
  if ! git rev-parse "$NEW_TAG" >/dev/null 2>&1; then
    echo "$NEW_TAG"
    break
  fi
done
