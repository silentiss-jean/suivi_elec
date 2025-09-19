def test_get_energy_entities_success(requests_mock):
    url = "http://localhost:8123/entities"
    token = "FAKE_TOKEN"

    mock_response = [
        {"entity_id": "sensor.energy_1", "state": "10", "attributes": {"device_class": "energy"}},
        {"entity_id": "sensor.energy_2", "state": "5", "attributes": {"device_class": "energy"}},
        {"entity_id": "sensor.temp", "state": "22", "attributes": {"device_class": "temperature"}}
    ]
    requests_mock.get(url, json=mock_response)

    from custom_components.suivi_elec.helpers.api_client import get_energy_entities
    result = get_energy_entities("http://localhost:8123", token)

    assert len(result) == 3
    assert any(e["entity_id"] == "sensor.energy_1" for e in result)
