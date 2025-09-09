#!/bin/bash

HELPERS_DIR="custom_components/suivi_elec/helpers"

echo "🔍 Scan des imports vers launcher dans $HELPERS_DIR"
echo "-----------------------------------------------"

FOUND=0

# Parcours de tous les fichiers .py dans helpers/
for file in "$HELPERS_DIR"/*.py; do
  while IFS= read -r line; do
    if echo "$line" | grep -q "launcher"; then
      echo "⚠️ Import suspect dans $file :"
      echo "   $line"
      FOUND=1
    fi
  done < "$file"
done

if [ "$FOUND" -eq 0 ]; then
  echo "✅ Aucun import vers launcher trouvé dans helpers/"
else
  echo "🚨 Vérifie les imports ci-dessus : utilise 'from ..launcher import ...' dans helpers/"
fi
