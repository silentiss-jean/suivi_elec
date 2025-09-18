from custom_components.suivi_elec.helpers.calculateur import calculer_cout

def test_calculer_cout_prix_unique():
    conso = 12.5
    contrat = {
        "type_contrat": "prix_unique",
        "prix_ht": 0.2,
        "abonnement_annuel": 120
    }
    result = calculer_cout(conso, contrat)
    assert result["total_ht"] == round(0.2 * 12.5 + 120 / 12, 2)

def test_calculer_cout_hp_hc():
    conso = {"hp": 10, "hc": 5}
    contrat = {
        "type_contrat": "heures_pleines_creuses",
        "prix_ht_hp": 0.25,
        "prix_ht_hc": 0.15,
        "abonnement_annuel": 120
    }
    result = calculer_cout(conso, contrat)
    total = 0.25 * 10 + 0.15 * 5 + 120 / 12
    assert result["total_ht"] == round(total, 2)
