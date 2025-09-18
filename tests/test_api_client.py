import custom_components.suivi_elec.helpers.api_client as api

def test_connection_returns_bool():
    """Vérifie que la fonction retourne bien un booléen, même avec des paramètres fictifs."""
    result = api.test_api_connection("http://localhost:8123", "abc123")
    assert isinstance(result, bool)
