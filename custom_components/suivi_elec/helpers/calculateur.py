def calculer_cout(entity, tarifs):
    try:
        raw_state = entity.get("state", "0")
        if raw_state in ["unavailable", "unknown", None]:
            raise ValueError(f"État non exploitable : {raw_state}")

        state = float(raw_state)
        entity_id = entity.get("entity_id", "inconnu")
        nom = entity.get("attributes", {}).get("friendly_name", entity_id)

        # 💡 Choix du tarif selon le type
        if "hc" in entity_id.lower():
            prix_kwh = tarifs.get("hc", tarifs["kwh"])
            mode = "heures creuses"
        elif "hp" in entity_id.lower():
            prix_kwh = tarifs.get("hp", tarifs["kwh"])
            mode = "heures pleines"
        else:
            prix_kwh = tarifs.get("kwh", 0.174)
            mode = "standard"

        total_ht = round(state * prix_kwh, 2)
        total_ttc = round(total_ht * 1.2, 2)  # TVA 20%
        return {
            "entity_id": entity_id,
            "nom": nom,
            "energie_kwh": round(state, 2),
            "prix_kwh": prix_kwh,
            "mode_tarif": mode,
            "total_ht": total_ht,
            "total_ttc": total_ttc
        }

    except Exception as e:
        print(f"⚠️ Ignoré {entity.get('entity_id', 'inconnu')} → {e}")
        return None
