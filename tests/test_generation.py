from custom_components.suivi_elec.helpers.generation import generate_yaml_config

def test_generate_yaml_config_basic():
    capteurs = ["sensor.device_1_power"]
    config = {"abonnement_annuel": 120}
    yaml = generate_yaml_config(capteurs, config)
    assert "sensor:" in yaml
    assert "input_number:" in yaml
    assert "template:" in yaml
    assert "Prix du kWh" in yaml
