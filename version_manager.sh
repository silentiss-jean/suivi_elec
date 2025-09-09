#!/bin/bash

MODE=$1

if [ "$MODE" == "dev" ]; then
  # 🔧 Génère une version de dev basée sur le dernier tag stable
  LAST_TAG=$(git tag --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | tail -n 1)
  BASE=${LAST_TAG:-v0.9.0}
  DATE=$(date +"%Y%m%d.%H%M")
  echo "${BASE}-dev.${DATE}"

elif [ "$MODE" == "stable" ]; then
  # 🔧 Incrémente le patch du dernier tag stable
  LAST_TAG=$(git tag --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | tail -n 1)

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

  echo "v${MAJOR}.${MINOR}.${PATCH}"

else
  echo "❌ Usage : ./version_manager.sh [dev|stable]" >&2
  exit 1
fi
