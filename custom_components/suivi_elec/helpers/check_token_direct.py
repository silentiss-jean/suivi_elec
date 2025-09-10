import requests

# 🔧 Renseigne ici ton URL et ton token
HA_URL = "http://192.168.3.160:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI0Yjg0NDM1YzU2MWU0MzNhODM2MmZjNWJiOWNmMTIzNiIsImlhdCI6MTc1NzUwNzU2MCwiZXhwIjoyMDcyODY3NTYwfQ.6jwks61eBLBiu4__i2LrF0INoZaJiUWq8IbnkfbA4x0"  # Remplace par ton vrai token

def test_token(url, token):
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(f"{url}/api/", headers=headers, timeout=5)
        print(f"🔗 Requête vers {url}/api/")
        print(f"📡 Statut HTTP : {response.status_code}")
        if response.status_code == 200:
            print("✅ Token valide, accès à l'API confirmé")
        elif response.status_code == 401:
            print("❌ Token invalide ou expiré (401 Unauthorized)")
        else:
            print(f"⚠️ Réponse inattendue : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de connexion à l'API : {e}")

test_token(HA_URL, HA_TOKEN)