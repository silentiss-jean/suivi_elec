import os
from dotenv import load_dotenv

def pytest_configure():
    env_path = os.path.join(os.path.dirname(__file__), "../custom_components/suivi_elec/.env")
    load_dotenv(dotenv_path=env_path)
