# -*- coding: utf-8 -*-
"""Utilitaires de détection pour Suivi Élec (mode, entités, contrat)."""

from .api_client import test_api_connection, get_energy_entities
from .const import DEFAULT_URL, DEFAULT_TOKEN, CONTRATS

def detect_mode(base_url=DEFAULT_URL, token=DEFAULT_TOKEN):
    """Détecte si l'instance est accessible en mode distant."""
    try:
        return "remote" if test_api_connection(base_url, token) else "local"
    except Exception:
        return "local"

def detect_entities(base_url=DEFAULT_URL, token=DEFAULT_TOKEN):
    """Retourne une liste d'entités énergétiques détectées."""
    try:
        entities = get_energy_entities(base_url, token)
        return [e["entity_id"] for e in entities] if entities else []
    except Exception:
        return []

def suggest_contract(entities):
    """Suggère un contrat tarifaire selon les entités détectées."""
    has_hp = any("hp" in e.lower() for e in entities)
    has_hc = any("hc" in e.lower() for e in entities)
    return "heures_pleines_creuses" if has_hp and has_hc else "prix_unique"