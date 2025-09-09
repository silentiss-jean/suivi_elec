import os
import requests
import json
from dotenv import load_dotenv

# 🔐 Charge les variables d'environnement depuis .env
load_dotenv()

# 🔧 Configuration Home Assistant
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json"
}

# 🧪 Exemple de requête GET vers Home Assistant
def get_states():
    url = f"{HA_URL}/api/states"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur {response.status_code} : {response.text}")
        return None

# 🧪 Exemple d'utilisation
if __name__ == "__main__":
    states = get_states()
    if states:
        print(json.dumps(states, indent=2))