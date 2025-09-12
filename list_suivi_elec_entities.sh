#!/bin/bash

# Charger les variables depuis .env
set -a
source .env
set +a

echo "🔍 Liste des entités marquées par Suivi Élec (integration: suivi_elec)"
echo "---------------------------------------------------------------"

curl -s -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" "$HA_URL/api/states" \
| jq '.[] | select(.attributes.integration == "suivi_elec") | .entity_id'
