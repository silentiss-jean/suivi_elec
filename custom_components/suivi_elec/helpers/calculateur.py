def calculer_cout(entity, tarifs):
    try:
        state = entity["state"]
        if state in ["unavailable", "unknown", None]:
            return None
        energie = float(state)
        cout_ht = round(energie * tarifs["tarif_ht"], 4)
        cout_ttc = round(energie * tarifs["tarif_ttc"], 4)
        total_ht = round(cout_ht + tarifs["abonnement_ht"], 4)
        total_ttc = round(cout_ttc + tarifs["abonnement_ttc"], 4)
        return {
            "entity_id": entity["entity_id"],
            "energie_kwh": energie,
            "cout_ht": cout_ht,
            "cout_ttc": cout_ttc,
            "total_ht": total_ht,
            "total_ttc": total_ttc
        }
    except Exception as e:
        print(f"❌ Erreur calcul coût pour {entity['entity_id']}: {e}")
        return None