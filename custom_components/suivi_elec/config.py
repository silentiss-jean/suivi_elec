import yaml
import os

# 📍 Chemin du fichier settings.yaml (dans le même dossier que config.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.yaml")

# 📦 Chargement sécurisé du fichier settings.yaml
try:
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = yaml.safe_load(f) or {}
except FileNotFoundError:
    print(f"⚠️ Fichier settings.yaml introuvable à : {SETTINGS_PATH}. Utilisation des valeurs par défaut.")
    settings = {}
except yaml.YAMLError as e:
    raise ValueError(f"❌ Erreur de parsing YAML dans settings.yaml : {e}")

# 🔧 Paramètres généraux
HA_URL = settings.get("ha_url", "http://homeassistant.local:8123")
HA_TOKEN = settings.get("ha_token", "TON_TOKEN_ICI")

# 📁 Fichiers internes
FICHIER_CAPTEURS = "data/capteurs_detectes.json"
FICHIER_NOMS_PERSONNALISES = "settings/noms_personnalises.yaml"
FICHIER_GROUPES_ENERGY = "data/groupes_capteurs_energy.py"
FICHIER_GROUPES_POWER = "data/groupes_capteurs_power.py"

# 🧠 Device classes à surveiller
DEVICE_CLASSES_UTILISEES = settings.get("device_classes_utilisees", ["energy", "power", "current", "voltage"])

# 🧩 Mots-clés par défaut pour regroupement automatique
PIECES_PAR_DEFAUT = settings.get("pieces_par_defaut", {
    "salon": "Salon",
    "chambre": "Chambre",
    "cuisine": "Cuisine",
    "buanderie": "Buanderie",
    "bureau": "Bureau",
    "clim": "Climatisation",
    "radiateur": "Radiateur"
})

# 🔠 Entités input_text dans Home Assistant
INPUT_TEXT_ENTITES = settings.get("input_text_entites", [
    "input_text.nom_emma",
    "input_text.nom_dalex",
    "input_text.nom_chambre",
    "input_text.nom_salon",
    "input_text.nom_cuisine",
    "input_text.nom_buanderie",
    "input_text.nom_bureau",
    "input_text.nom_radiateur",
    "input_text.nom_clim"
])