# -*- coding: utf-8 -*-
"""Script principal de génération pour l'intégration suivi_elec.

Génère :
 - package HA (suivi_elec.yaml)
 - carte Lovelace grid (lovelace_conso.yaml)
 - carte history (lovelace_history_conso.yaml)

Principales améliorations :
 - noms d'entités "slugifiés" (pas d'accents / caractères spéciaux)
 - déduplication des capteurs
 - validation de base (doit commencer par 'sensor.')
 - utilisation cohérente des noms d'entités générés
 - logging et écriture UTF-8
"""

from __future__ import annotations
import os
import re
import unicodedata
import logging
from pathlib import Path
from typing import Dict, List

from .helpers import regroupement, loader, install_helper

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())

# Mappings
CYCLE_MAP = {"jour": "daily", "semaine": "weekly", "mois": "monthly", "annee": "yearly"}
TITRE_DISPLAY = {"jour": "Aujourd'hui", "semaine": "Semaine", "mois": "Mois", "annee": "Annee"}
TITRE_ENTITY = {"jour": "aujourdhui", "semaine": "semaine", "mois": "mois", "annee": "annee"}


def slugify(value: str) -> str:
    """Retourne une version 'safe' pour entity_id: ascii, lowercase, underscores."""
    value = str(value)
    # remove accents
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    # remove invalid chars
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    # spaces/dashes -> underscore
    value = re.sub(r"[-\s]+", "_", value)
    return value


def normalize_name(entity_id: str) -> str:
    """Normalise un entity_id sensor.xxx -> base slug (sans 'sensor.' ni suffixes)."""
    if not isinstance(entity_id, str):
        return ""
    base = entity_id.replace("sensor.", "")
    base = base.replace("_power", "").replace("_puissance", "")
    return slugify(base)


def _write_file(path: Path, content: str) -> None:
    """Écrit en utf-8 et logge."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(content)
    _LOGGER.info("Fichier écrit : %s", path)


def _unique_preserve_order(seq: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def generate_yaml_config(capteurs: List[str]) -> str:
    """Génère le contenu YAML du package (string)."""
    lines: List[str] = []
    lines.append("####################################")
    lines.append("# Package suivi électricité (auto)")
    lines.append("####################################\n")

    # input_number prix
    lines.append("input_number:")
    lines.append("  prix_kwh:")
    lines.append("    name: Prix du kWh")
    lines.append("    min: 0")
    lines.append("    max: 1")
    lines.append("    step: 0.001")
    lines.append("    unit_of_measurement: \"€/kWh\"")
    lines.append("    initial: 0.25")
    lines.append("    mode: box\n")

    # sensors integration (energy)
    lines.append("sensor:")
    for c in capteurs:
        if not isinstance(c, str) or not c.startswith("sensor."):
            _LOGGER.warning("Capteur ignoré (non sensor.*) : %s", c)
            continue
        name = normalize_name(c)
        if not name:
            continue
        lines.append(f"  - platform: integration")
        lines.append(f"    source: {c}")
        lines.append(f"    name: energy_{name}")
        lines.append(f"    unit_prefix: k")
        lines.append(f"    round: 2")
        lines.append(f"    method: trapezoidal\n")

    # utility_meter
    lines.append("utility_meter:")
    for c in capteurs:
        if not isinstance(c, str) or not c.startswith("sensor."):
            continue
        name = normalize_name(c)
        if not name:
            continue
        for cycle, yaml_cycle in CYCLE_MAP.items():
            lines.append(f"  energy_{name}_{cycle}:")
            lines.append(f"    source: sensor.energy_{name}")
            lines.append(f"    cycle: {yaml_cycle}\n")

    # template sensors (couts)
    lines.append("template:")
    lines.append("  - sensor:")
    for c in capteurs:
        if not isinstance(c, str) or not c.startswith("sensor."):
            continue
        name = normalize_name(c)
        if not name:
            continue
        pretty = name.replace("_", " ").title()  # human readable part
        for cycle in ["jour", "semaine", "mois", "annee"]:
            # display name (human), entity id will be slugify(name_display)
            display_name = f"Cout {pretty} {TITRE_DISPLAY[cycle]}"
            # We rely on slugify(display_name) to be the resulting entity_id (sensor.xxx)
            lines.append(f"      - name: \"{display_name}\"")
            lines.append(f"        unit_of_measurement: \"€\"")
            lines.append("        state: >")
            # jinja lines (use normal concatenation to avoid f-string braces issues)
            lines.append("          {% set prix = states('input_number.prix_kwh') | float(0) %}")
            lines.append("          {% set conso = states('sensor.energy_" + name + "_" + cycle + "') | float(0) %}")
            lines.append("          {{ (prix * conso) | round(2) }}\n")

    return "\n".join(lines)


def generate_lovelace_grid(groupes: Dict[str, List[str]], mode: str) -> str:
    """Génère une carte Lovelace 'grid' Markdown/Entities pour la conso."""
    lines: List[str] = []
    lines.append("type: vertical-stack")
    lines.append("cards:")
    for groupe, capteurs in groupes.items():
        lines.append("  - type: grid")
        # Display group title safe
        group_title = groupe
        lines.append(f"    title: {group_title}")
        lines.append("    columns: 2")
        lines.append("    cards:")
        for c in capteurs:
            if not isinstance(c, str) or not c.startswith("sensor."):
                continue
            name = normalize_name(c)
            pretty = name.replace("_", " ").title()
            for cycle in ["jour", "semaine", "mois", "annee"]:
                # cost entity id derived from display name used in template creation
                display_cost_name = f"Cout {pretty} {TITRE_DISPLAY[cycle]}"
                cost_entity_id = "sensor." + slugify(display_cost_name)
                energy_entity_id = f"sensor.energy_{name}_{cycle}"
                lines.append("      - type: entities")
                lines.append(f"        title: {pretty} – {TITRE_DISPLAY[cycle]}")
                lines.append("        entities:")
                if mode == "energy":
                    lines.append(f"          - entity: {energy_entity_id}")
                    lines.append(f"            name: Consommation")
                    lines.append(f"          - entity: {cost_entity_id}")
                    lines.append(f"            name: Coût")
                else:
                    lines.append(f"          - entity: {c}")
                    lines.append(f"            name: Puissance")
    return "\n".join(lines)


def generate_history_card(groupes: Dict[str, List[str]], mode: str) -> str:
    """Génère une configuration YAML pour la carte history-explorer (bar)."""
    lines: List[str] = []
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
            if not isinstance(c, str) or not c.startswith("sensor."):
                continue
            name = normalize_name(c)
            label = name.replace("_", " ").title()
            if mode == "energy":
                # we display cost sensors aggregated per day
                cost_display = f"Cout {label} {TITRE_DISPLAY['jour']}"
                cost_entity = "sensor." + slugify(cost_display)
                lines.append(f"      - entity: {cost_entity}")
            else:
                lines.append(f"      - entity: {c}")
            lines.append(f"        name: {label}")
    lines.append("grid_options:")
    lines.append("  columns: 3")
    lines.append("  rows: null")
    return "\n".join(lines)


def run_all(mode_force: str = None) -> None:
    """Exécution principale : génère les fichiers en se basant sur les groupes détectés."""
    _LOGGER.info("Lancement du script suivi_elec")
    # Regroupe les capteurs (ton helper)
    regroupement.regroupe_capteurs()

    # Charger les groupes (structure dict: groupe -> [entity_id, ...])
    groupes = loader.charger_groupes("groupes_capteurs_energy")
    if not isinstance(groupes, dict):
        _LOGGER.error("loader.charger_groupes n'a pas retourné un dict, annulation.")
        return

    # choisir mode (energy by default) ou override par param
    mode = mode_force or "energy"

    # flatten et dedupe capteurs (ordre préservé)
    all_capteurs = [item for sub in groupes.values() for item in sub]
    all_capteurs = _unique_preserve_order(all_capteurs)

    # dossier cible (via ton helper)
    dossier_cible_str = install_helper.choisir_emplacement_fichiers(mode_force=mode)
    dossier_cible = Path(dossier_cible_str)

    # Générer YAML package
    yaml_config = generate_yaml_config(all_capteurs)
    _write_file(dossier_cible / "suivi_elec.yaml", yaml_config)

    # Générer Lovelace grid
    lovelace_card = generate_lovelace_grid(groupes, mode)
    _write_file(dossier_cible / "lovelace_conso.yaml", lovelace_card)

    # Générer history card
    history_card = generate_history_card(groupes, mode)
    _write_file(dossier_cible / "lovelace_history_conso.yaml", history_card)

    _LOGGER.info("✅ Fichiers générés automatiquement en mode '%s' dans %s", mode, dossier_cible)
    print(f"✅ Fichiers générés automatiquement en mode '{mode}' dans {dossier_cible}")