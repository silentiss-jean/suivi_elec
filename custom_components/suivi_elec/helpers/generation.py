# -*- coding: utf-8 -*-
import os
from datetime import datetime
from calculateur import est_hp

generate_yaml = True
generate_lovelace = True
generate_history = True

if generate_yaml:
    from groupes_capteurs_energy import groupes
    mode = "energy"
else:
    from groupes_capteurs_power import groupes
    mode = "power"

def normalize_name(entity_id: str) -> str:
    base = entity_id.replace("sensor.", "").replace("_power", "").replace("_puissance", "")
    return base.lower()

def generate_yaml_config(capteurs, config_data: dict = None) -> str:
    config_data = config_data or {}
    lines = [
        "####################################",
        "# Package suivi électricité (auto)",
        "####################################\n"
    ]

    lines += [
        "input_number:",
        "  prix_kwh:",
        "    name: Prix du kWh",
        "    min: 0",
        "    max: 1",
        "    step: 0.001",
        "    unit_of_measurement: \"€/kWh\"",
        "    initial: 0.25",
        "    mode: box\n"
    ]

    lines.append("sensor:")
    for c in capteurs:
        name = normalize_name(c)
        lines += [
            f"  - platform: integration",
            f"    source: {c}",
            f"    name: energy_{name}",
            "    unit_prefix: k",
            "    round: 2",
            "    method: trapezoidal\n"
        ]

    cycle_map = {'jour': 'daily', 'semaine': 'weekly', 'mois': 'monthly', 'annee': 'yearly'}
    for c in capteurs:
        name = normalize_name(c)
        for cycle, cycle_value in cycle_map.items():
            lines += [
                f"  energy_{name}_{cycle}:",
                f"    source: sensor.energy_{name}",
                f"    cycle: {cycle_value}\n"
            ]

    lines.append("template:")
    lines.append("  - sensor:")
    titre_map = {"jour": "aujourdhui", "semaine": "semaine", "mois": "mois", "annee": "annee"}
    for c in capteurs:
        name = normalize_name(c)
        pretty = name.replace("_", " ").title()
        for cycle, titre in titre_map.items():
            lines += [
                f"      - name: \"Cout {pretty} {titre}\"",
                "        unit_of_measurement: \"€\"",
                "        state: >",
                "          {% set prix = states('input_number.prix_kwh') | float(0) %}",
                f"          {{% set conso = states('sensor.energy_{name}_{cycle}') | float(0) %}}",
                "          {% set abonnement = " +
                f"{config_data.get('abonnement_annuel',0) if config_data else 0} %}",
                "          {{ (prix * conso + abonnement/12) | round(2) }}\n"
            ]

    return "\n".join(lines)

# Les fonctions generate_lovelace_grid et generate_history_card restent identiques à ce que tu avais
# pour générer les cartes et historiques

def run_all(config_data=None):
    all_capteurs = [item for sublist in groupes.values() for item in sublist]
    dossier_cible = "/data"

    if generate_yaml:
        yaml_config = generate_yaml_config(all_capteurs, config_data)
        with open(os.path.join(dossier_cible, "suivi_elec.yaml"), "w", encoding="utf-8") as f:
            f.write(yaml_config)

    print(f"✅ Fichiers générés automatiquement en mode '{mode}'")

if __name__ == "__main__":
    run_all()