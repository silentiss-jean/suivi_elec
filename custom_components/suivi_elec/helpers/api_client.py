# -*- coding: utf-8 -*-
"""Client API pour Suivi Élec : test de connexion et récupération des entités énergétiques."""

import requests
from requests.exceptions import RequestException, Timeout

DEFAULT_TIMEOUT = 5  # secondes

def test_api_connection(base_url: str, token: str) -> bool:
    """Teste la connexion à l'API distante avec le jeton fourni."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/ping", headers=headers, timeout=DEFAULT_TIMEOUT)
        return response.status_code == 200
    except (RequestException, Timeout):
        return False

def get_energy_entities(base_url: str, token: str):
    """Récupère les entités énergétiques disponibles via l'API distante."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/entities", headers=headers, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            # On attend une liste de dicts avec une clé 'entity_id'
            return [e for e in data if "entity_id" in e]
        return None
    except (RequestException, Timeout, ValueError):
        return None