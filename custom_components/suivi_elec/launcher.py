# -*- coding: utf-8 -*-
# Script principal intelligent : choisit automatiquement le bon fichier de capteurs

import os
from .helpers import regroupement, loader

def normalize_name(entity_id):
    base = entity_id.replace("sensor.", "").replace("_power", "").replace("_puissance", "")
    return base.lower()

def generate_yaml_config(capteurs):
    lines = []
    lines.append("####################################")
    lines.append("# Package suivi électricité (auto)")
    lines.append("####################################\n")

    lines.append("input_number:")
    lines.append("  prix_kwh:")
    lines.append("    name: Prix du kWh")
    lines.append("    min: 0")
    lines.append("    max: 1")
    lines.append("    step: 0.001")
    lines.append("    unit_of_measurement: \"€/kWh\"")
    lines.append("    initial: 0.25")
    lines.append("    mode: box\n")

    lines.append("sensor:")
    for c in capteurs:
        name = normalize_name(c)
        lines.append(f"  - platform: integration")
        lines.append(f"    source: {c}")
        lines.append(f"    name: energy_{name}")
        lines.append(f"    unit_prefix: k")
        lines.append(f"    round: 2")
        lines.append(f"    method: trapezoidal\n")

    lines.append("utility_meter:")
    cycle_map = {'jour': 'daily', 'semaine': 'weekly', 'mois': 'monthly', 'annee': 'yearly'}
    for c in capteurs:
        name = normalize_name(c)
        for cycle, cycle_value in cycle_map.items():
            lines.append(f"  energy_{name}_{cycle}:")
            lines.append(f"    source: sensor.energy_{name}")
            lines.append(f"    cycle: {cycle_value}\n")

    lines.append("template:")
    lines.append("  - sensor:")
    titre_map = {"jour": "aujourdhui", "semaine": "semaine", "mois": "mois", "annee": "annee"}
    for c in capteurs:
        name = normalize_name(c)
        pretty = name.replace("_", " ").title()
        for cycle, titre in titre_map.items():
            lines.append(f"      - name: \"Cout {pretty} {titre}\"")
            lines.append(f"        unit_of_measurement: \"€\"")
            lines.append("        state: >")
            lines.append("          {% set prix = states('input_number.prix_kwh') | float(0) %}")
            lines.append(f"          {{% set conso = states('sensor.energy_{name}_{cycle}') | float(0) %}}")
            lines.append(f"          {{ (prix * conso) | round(2) }}\n")

    return "\n".join(lines)

def generate_lovelace_grid(groupes, mode):
    lines = []
    lines.append("type: vertical-stack")
    lines.append(f"title: ⚡ Suivi {'instantané' if mode == 'power' else 'coût'} par pièce")
    lines.append("cards:")

    titre_map = {"jour": "Jour", "semaine": "Semaine", "mois": "Mois", "annee": "Année"}

    for groupe, capteurs in groupes.items():
        lines.append(f"  - type: grid")
        lines.append(f"    title: {groupe}")
        lines.append("    columns: 2")
        lines.append("    cards:")

        for c in capteurs:
            name = normalize_name(c)
            pretty = name.replace("_", " ").title()

            for cycle, titre in titre_map.items():
                lines.append("      - type: entities")
                lines.append(f"        title: {pretty} – {titre}")
                lines.append("        entities:")
                if mode == "energy":
                    lines.append(f"          - entity: sensor.energy_{name}_{cycle}")
                    lines.append(f"            name: Consommation {titre}")
                    lines.append(f"          - entity: sensor.cout_{name}_{'aujourdhui' if cycle == 'jour' else cycle}")
                    lines.append(f"            name: Coût {titre}")
                else:
                    lines.append(f"          - entity: {c}")
                    lines.append(f"            name: Puissance")

    return "\n".join(lines)

def generate_history_card(groupes, mode):
    lines = []
    lines.append("type: custom:history-explorer-card")
    lines.append(f'header: "📈 Historique des {"puissances" if mode == "power" else "coûts"} par pièce"')
    lines.append("graphs:")

    for groupe, capteurs in groupes.items():
        lines.append("  - type: bar")
        lines.append(f"    title: {groupe}")
        lines.append("    options:")
        lines.append("      interval: hour")
        lines.append("      stacked: true")
        lines.append("    entities:")

        for c in capteurs:
            name = normalize_name(c)
            label = name.replace("_", " ").title()
            if mode == "energy":
                lines.append(f"      - entity: sensor.cout_{name}_aujourdhui")
            else:
                lines.append(f"      - entity: {c}")
            lines.append(f"        name: {label}")

    lines.append("grid_options:")
    lines.append("  columns: 3")
    lines.append("  rows: null")

    return "\n".join(lines)

def run_all():
    # 🔄 Mise à jour des fichiers de groupes
    regroupement.regroupe_capteurs()

    # 🔍 Détection du besoin selon les fichiers à générer
    generate_yaml = True
    generate_lovelace = True
    generate_history = True

    # 📦 Chargement dynamique du bon fichier
    if generate_yaml:
        groupes = loader.charger_groupes("groupes_capteurs_energy")
        mode = "energy"
    else:
        groupes = loader.charger_groupes("groupes_capteurs_power")
        mode = "power"

    all_capteurs = [item for sublist in groupes.values() for item in sublist]

    if generate_yaml:
        yaml_config = generate_yaml_config(all_capteurs)
        with open("/config/suivi_elec.yaml", "w", encoding="utf-8") as f:
            f.write(yaml_config)

    if generate_lovelace:
        lovelace_card = generate_lovelace_grid(groupes, mode)
        with open("/config/lovelace_conso.yaml", "w", encoding="utf-8") as f:
            f.write(lovelace_card)

    if generate_history:
        history_card = generate_history_card(groupes, mode)
        with open("/config/lovelace_history_conso.yaml", "w", encoding="utf-8") as f:
            f.write(history_card)

    print(f"✅ Fichiers générés automatiquement en mode '{mode}'")