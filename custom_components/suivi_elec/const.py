# -*- coding: utf-8 -*-
"""Constantes globales pour l'intégration Suivi Élec."""

DOMAIN = "suivi_elec"

# 🔑 Clés de configuration
CONF_NAME = "name"
CONF_MODE = "mode"
CONF_TOKEN = "token"
CONF_URL = "base_url"
CONF_TYPE_CONTRAT = "type_contrat"
CONF_PRIX_HT = "prix_ht"
CONF_PRIX_TTC = "prix_ttc"
CONF_PRIX_HT_HP = "prix_ht_hp"
CONF_PRIX_TTC_HP = "prix_ttc_hp"
CONF_PRIX_HT_HC = "prix_ht_hc"
CONF_PRIX_TTC_HC = "prix_ttc_hc"
CONF_HEURE_DEBUT_HP = "heure_debut_hp"
CONF_HEURE_FIN_HP = "heure_fin_hp"
CONF_ABONNEMENT_ANNUEL = "abonnement_annuel"

# 🧰 Valeurs par défaut
DEFAULT_NAME = "Suivi Électricité"
DEFAULT_MODE = "local"
DEFAULT_URL = "http://homeassistant.local:8123"
DEFAULT_REMOTE_URL = "https://api.edf.fr"
DEFAULT_TOKEN = ""
DEFAULT_PRIX_HT = 0.15
DEFAULT_PRIX_HT_HP = 0.18
DEFAULT_PRIX_HT_HC = 0.12
DEFAULT_ABONNEMENT = 0.0

# 📦 Types de contrat
CONTRATS = ["prix_unique", "heures_pleines_creuses"]

# 📊 Entités par défaut (à personnaliser si besoin)
ENTITES_POTENTIELLES = [
    "sensor.machine_a_laver_energy",
    "sensor.frigo_energy",
    "sensor.television_energy",
    "sensor.ordinateur_energy",
    "sensor.chauffage_energy"
]