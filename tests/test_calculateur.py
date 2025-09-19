from datetime import datetime
from custom_components.suivi_elec.helpers.calculateur import calculer_cout

def test_calcul_prix_unique():
    entity = {
        "entity_id": "sensor.test_energy",
        "state": "12.5",
        "attributes": {"friendly_name": "Test Energy"}
    }
    tarifs = {
        "type_contrat": "prix_unique",
        "prix_ht": 0.20,
        "prix_ttc": 0.24,
        "abonnement_annuel": 120.0
    }
    result = calculer_cout(entity, tarifs, datetime(2025, 9, 19), inclure_abonnement=True, periode="mois")
    assert result["total_ht"] == round(12.5 * 0.20 + 10.0, 2)  # 10.0 = 120 / 12
    assert result["total_ttc"] == round(12.5 * 0.24 + 12.0, 2)  # 12.0 = 120 * 1.2 / 12
    assert result["mode_tarif"] == "prix unique"

def test_calcul_hp_hc_hp():
    entity = {
        "entity_id": "sensor.test_energy",
        "state": "5",
        "attributes": {"friendly_name": "Test HP"}
    }
    tarifs = {
        "type_contrat": "heures_pleines_creuses",
        "hp": {"prix_ht": 0.30, "prix_ttc": 0.36, "debut": "06:00", "fin": "22:00"},
        "hc": {"prix_ht": 0.15, "prix_ttc": 0.18, "debut": "22:00", "fin": "06:00"},
        "abonnement_annuel": 0.0
    }
    result = calculer_cout(entity, tarifs, datetime(2025, 9, 19, 10, 0))
    assert result["total_ht"] == 1.5
    assert result["total_ttc"] == 1.8
    assert result["mode_tarif"] == "heures pleines"

def test_calcul_hp_hc_hc():
    entity = {
        "entity_id": "sensor.test_energy",
        "state": "5",
        "attributes": {"friendly_name": "Test HC"}
    }
    tarifs = {
        "type_contrat": "heures_pleines_creuses",
        "hp": {"prix_ht": 0.30, "prix_ttc": 0.36, "debut": "06:00", "fin": "22:00"},
        "hc": {"prix_ht": 0.15, "prix_ttc": 0.18, "debut": "22:00", "fin": "06:00"},
        "abonnement_annuel": 0.0
    }
    result = calculer_cout(entity, tarifs, datetime(2025, 9, 19, 23, 0))
    assert result["total_ht"] == 0.75
    assert result["total_ttc"] == 0.9
    assert result["mode_tarif"] == "heures creuses"
