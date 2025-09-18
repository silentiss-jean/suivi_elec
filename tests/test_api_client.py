import os
from dotenv import load_dotenv
import requests_mock
import custom_components.suivi_elec.helpers.api_client as api

def test_connection_returns_bool():
    result = api.test_api_connection("http://localhost:8123", "abc123")
    assert isinstance(result, bool)

def test_get_energy_entities_with_env():
    """Teste que toutes les entités avec 'entity_id' sont bien retournées."""
    load_dotenv(dotenv_path="custom_components/suivi_elec/.env")

    base_url = os.getenv("HA_URL")
    token = os.getenv("HA_TOKEN")

    assert base_url is not None
    assert token is not None

    mock_data = [
        {"entity_id": "sensor.tv_energy"},
        {"entity_id": "sensor.frigo_energy"},
        {"entity_id": "sensor.lampe_power"},
        {"entity_id": "light.salon"}
    ]

    with requests_mock.Mocker() as m:
        m.get(f"{base_url}/entities", json=mock_data)
        result = api.get_energy_entities(base_url, token)

        assert isinstance(result, list)
        assert len(result) == 4
        assert all("entity_id" in e for e in result)
        assert {e["entity_id"] for e in result} == {
            "sensor.tv_energy",
            "sensor.frigo_energy",
            "sensor.lampe_power",
            "light.salon"
        }
