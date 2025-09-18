import os
from custom_components.suivi_elec.helpers.env_loader import load_env

def test_load_env(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("HA_URL=http://localhost\nHA_TOKEN=abc123\n")
    load_env(str(env_file))
    assert os.environ.get("HA_URL") == "http://localhost"
    assert os.environ.get("HA_TOKEN") == "abc123"
