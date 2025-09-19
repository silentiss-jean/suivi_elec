import pytest
from homeassistant.core import HomeAssistant
from custom_components.suivi_elec.detect_async import run_detect_async

@pytest.mark.asyncio
async def test_detect_async_creates_status_sensor(hass: HomeAssistant):
    # Simuler une entrée de configuration
    entry = type("MockEntry", (), {
        "data": {
            "base_url": "http://localhost:8123",
            "token": "FAKE_TOKEN",
            "mode": "local"
        },
        "options": {}
    })()

    # Appeler la fonction de détection
    await run_detect_async(hass, entry)

    # Vérifier que le capteur de statut a été créé
    state = hass.states.get("sensor.suivi_elec_status")
    assert state is not None
    assert "entites_actives" in state.attributes
    assert state.state.startswith("local |")
