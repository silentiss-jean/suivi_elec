DOMAIN = "suivi_elec"
CONF_API_TOKEN = "api_token"
CONF_BASE_URL = "base_url"

# Clés pour les tarifs
CONF_KWH = "kwh"
CONF_HP = "hp"
CONF_HC = "hc"

ENTITES_POTENTIELLES = [
    "sensor.suivi_elec_conso_jour",
    "sensor.suivi_elec_cout_jour",
    "sensor.suivi_elec_tarif_actuel",
    "sensor.suivi_elec_conso_mois",
    "sensor.suivi_elec_cout_mois",
    "binary_sensor.suivi_elec_anomalie"
]
