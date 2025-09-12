#!/bin/bash

echo "📤 Export des entités Suivi Élec"
echo "--------------------------------"

EXPORT_FILE="/config/suivi_elec/backups/entities_export.json"
mkdir -p /config/suivi_elec/backups
echo "{" > "$EXPORT_FILE"

ENTITIES=$(ha entity list | grep suivi_elec)

for entity in $ENTITIES; do
    state=$(ha entity get "$entity" --state | jq -r '.state')
    attrs=$(ha entity get "$entity" --attributes | jq -c '.')
    echo "  \"$entity\": {\"state\": \"$state\", \"attributes\": $attrs}," >> "$EXPORT_FILE"
done

# Supprimer la dernière virgule pour validité JSON
sed -i '$ s/,$//' "$EXPORT_FILE"
echo "}" >> "$EXPORT_FILE"

echo "✅ Export terminé → $EXPORT_FILE"
