# -*- coding: utf-8 -*-
"""
Script principal complet pour Suivi Élec :
- Génère YAML pour Home Assistant
- Crée cartes Lovelace par pièce
- Crée carte historique (history-explorer)
- Support prix unique, HP/HC et abonnement annuel optionnel
"""

import os
from datetime import datetime
from groupes_capteurs_energy import groupes  # remplacer par groupes_capteurs_power si besoin
mode = "energy"  # ou 'power'

def normalize_name(entity_id: str) -> str:
    """Normalisation des noms de capteurs pour Home Assistant."""
    return entity_id.replace("sensor.", "").replace("_power", "").replace("_puissance", "").lower()

def generate_yaml_config(capteurs, config_data: dict = None) -> str:
    """Génère le YAML complet pour HA avec abonnement dynamique."""
    config_data = config_data or {}
    lines = [
        "####################################",
        "# Package suivi électricité (auto)",
        "####################################\n",
        "input_number:",
        "  prix_kwh:",
        "    name: Prix du kWh",
        "    min: 0",
        "    max: 1",
        "    step: 0.001",
        "    unit_of_measurement: \"€/kWh\"",
        "    initial: 0.25",
        "    mode: box\n",
        "sensor:"
    ]

    # Sensors d'intégration
    for c in capteurs:
        name = normalize_name(c)
        lines.extend([
            f"  - platform: integration",
            f"    source: {c}",
            f"    name: energy_{name}",
            "    unit_prefix: k",
            "    round: 2",
            "    method: trapezoidal\n"
        ])

    # Utility meters (jours, semaines, mois, année)
    cycles = {"jour": "daily", "semaine": "weekly", "mois": "monthly", "annee": "yearly"}
    for c in capteurs:
        name = normalize_name(c)
        for cycle, val in cycles.items():
            lines.extend([
                f"  energy_{name}_{cycle}:",
                f"    source: sensor.energy_{name}",
                f"    cycle: {val}\n"
            ])

    # Template pour coût avec abonnement dynamique
    lines.append("template:\n  - sensor:")
    titre_map = {"jour": "aujourdhui", "semaine": "semaine", "mois": "mois", "annee": "annee"}
    abonnement = config_data.get("abonnement_annuel", 0)
    for c in capteurs:
        name = normalize_name(c)
        pretty = name.replace("_", " ").title()
        for cycle, titre in titre_map.items():
            lines.extend([
                f"      - name: 'Cout {pretty} {titre}'",
                "        unit_of_measurement: '€'",
                "        state: >",
                "          {% set prix = states('input_number.prix_kwh') | float(0) %}",
                f"          {{% set conso = states('sensor.energy_{name}_{cycle}') | float(0) %}}",
                f"          {{ (prix * conso + {abonnement}/12) | round(2) }}\n"
            ])
    return "\n".join(lines)

def generate_lovelace_grid(groupes):
    """Carte Lovelace par pièce et par cycle."""
    lines = [
        "type: vertical-stack",
        f"title: ⚡ Suivi {'instantané' if mode=='power' else 'coût'} par pièce",
        "cards:"
    ]
    titre_map = {"jour": "Jour", "semaine": "Semaine", "mois": "Mois", "annee": "Année"}
    for groupe, capteurs in groupes.items():
        lines.extend([
            f"  - type: grid",
            f"    title: {groupe}",
            "    columns: 2",
            "    cards:"
        ])
        for c in capteurs:
            name = normalize_name(c)
            pretty = name.replace("_", " ").title()
            for cycle, titre in titre_map.items():
                lines.extend([
                    "      - type: entities",
                    f"        title: {pretty} – {titre}",
                    "        entities:"
                ])
                if mode == "energy":
                    lines.extend([
                        f"          - entity: sensor.energy_{name}_{cycle}",
                        f"            name: Consommation {titre}",
                        f"          - entity: sensor.cout_{name}_{'aujourdhui' if cycle=='jour' else cycle}",
                        f"            name: Coût {titre}"
                    ])
                else:
                    lines.append(f"          - entity: {c}\n            name: Puissance")
    return "\n".join(lines)

def generate_history_card(groupes):
    """Carte historique pour energy ou power."""
    lines = [
        "type: custom:history-explorer-card",
        f'header: "📈 Historique des {"puissances" if mode=="power" else "coûts"} par pièce"',
        "graphs:"
    ]
    for groupe, capteurs in groupes.items():
        lines.extend([
            "  - type: bar",
            f"    title: {groupe}",
            "    options:",
            "      interval: hour",
            "      stacked: true",
            "    entities:"
        ])
        for c in capteurs:
            name = normalize_name(c)
            label = name.replace("_", " ").title()
            if mode == "energy":
                lines.append(f"      - entity: sensor.cout_{name}_aujourdhui\n        name: {label}")
            else:
                lines.append(f"      - entity: {c}\n        name: {label}")
    lines.extend([
        "grid_options:",
        "  columns: 3",
        "  rows: null"
    ])
    return "\n".join(lines)

def run_all(config_data=None):
    """Génère tous les fichiers YAML et cartes Lovelace / history."""
    all_capteurs = [item for sublist in groupes.values() for item in sublist]
    dossier_cible = "data"
    os.makedirs(dossier_cible, exist_ok=True)

    # YAML
    yaml_config = generate_yaml_config(all_capteurs, config_data)
    with open(os.path.join(dossier_cible, "suivi_elec.yaml"), "w", encoding="utf-8") as f:
        f.write(yaml_config)

    # Lovelace
    lovelace_card = generate_lovelace_grid(groupes)
    with open(os.path.join(dossier_cible, "lovelace_conso.yaml"), "w", encoding="utf-8") as f:
        f.write(lovelace_card)

    # History
    history_card = generate_history_card(groupes)
    with open(os.path.join(dossier_cible, "lovelace_history_conso.yaml"), "w", encoding="utf-8") as f:
        f.write(history_card)

    print(f"✅ Tous les fichiers générés dans '{dossier_cible}' en mode '{mode}'")

if __name__ == "__main__":
    run_all(config_data={"abonnement_annuel": 120})