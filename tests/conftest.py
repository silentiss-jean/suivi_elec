import pytest

class FakeStates:
    def __init__(self):
        self._states = {}

    def async_set(self, entity_id, state, attributes=None):
        self._states[entity_id] = {
            "state": state,
            "attributes": attributes or {}
        }

    def get(self, entity_id):
        state = self._states.get(entity_id)
        if state:
            return type("State", (), state)
        return None

class FakeHass:
    def __init__(self):
        self.states = FakeStates()

@pytest.fixture
def hass():
    return FakeHass()

import sys
import os

# Ajouter le dossier racine au PYTHONPATH
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_path)
