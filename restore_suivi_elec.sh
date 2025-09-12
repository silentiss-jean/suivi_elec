#!/bin/bash

echo "♻️ Restauration des entités Suivi Élec depuis la sauvegarde"
echo "-----------------------------------------------------------"

BACKUP_FILE="/config/suivi_elec/backups/entities_backup.json"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Fichier de sauvegarde introuvable : $BACKUP_FILE"
    exit 1
fi

ENTITIES=$(jq -r 'keys[]' "$BACKUP_FILE")

for entity in $ENTITIES; do
    # Vérifier si l'entité existe déjà
    if ha entity get "$entity" &>/dev/null; then
        echo "⏩ Entité déjà existante : $entity → ignorée"
        continue
    fi

    state=$(jq -r --arg e "$entity" '.[$e].state' "$BACKUP_FILE")
    attrs=$(jq -c --arg e "$entity" '.[$e].attributes' "$BACKUP_FILE")

    echo "🔄 Recréation de $entity → état: $state"
    ha entity create "$entity" --state "$state" --attributes "$attrs" 2>/dev/null
done

echo "✅ Restauration terminée."
