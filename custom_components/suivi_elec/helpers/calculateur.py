# -*- coding: utf-8 -*-
from datetime import datetime

def est_hp(timestamp: datetime, hp_start: str, hp_end: str) -> bool:
    """Retourne True si l'heure est dans la plage HP (gestion chevauchement minuit)."""
    start = datetime.strptime(hp_start, "%H:%M").time()
    end = datetime.strptime(hp_end, "%H:%M").time()
    current = timestamp.time()
    if start < end:
        return start <= current < end
    else:
        return current >= start or current < end

def calculer_cout(entity: dict, tarifs: dict, timestamp: datetime = None,
                   inclure_abonnement: bool = False, periode: str = "mois") -> dict | None:
    """
    Calcul du coût d'une entité selon le type de contrat et l'abonnement.

    Args:
        entity: dict avec 'state', 'entity_id' et 'attributes'
        tarifs: dict avec configuration des prix et HP/HC
        timestamp: datetime pour déterminer HP/HC
        inclure_abonnement: bool, inclure ou non l'abonnement annuel
        periode: 'jour', 'semaine', 'mois', 'annee', pour répartir l'abonnement
    """
    try:
        raw_state = entity.get("state", 0)
        state = float(raw_state) if raw_state not in ["unknown", "unavailable", None, ""] else 0.0

        total_ht = 0.0
        total_ttc = 0.0
        mode = "standard"

        timestamp = timestamp or datetime.now()
        contrat = tarifs.get("type_contrat", "prix_unique")

        if contrat == "prix_unique":
            prix_ht = float(tarifs.get("prix_ht", 0))
            prix_ttc = float(tarifs.get("prix_ttc", prix_ht * 1.2))
            mode = "prix unique"
        else:
            hp = tarifs.get("hp", {})
            hc = tarifs.get("hc", {})
            hp_debut = hp.get("debut", "06:00")
            hp_fin = hp.get("fin", "22:00")
            if est_hp(timestamp, hp_debut, hp_fin):
                prix_ht = float(hp.get("prix_ht", 0))
                prix_ttc = float(hp.get("prix_ttc", prix_ht * 1.2))
                mode = "heures pleines"
            else:
                prix_ht = float(hc.get("prix_ht", 0))
                prix_ttc = float(hc.get("prix_ttc", prix_ht * 1.2))
                mode = "heures creuses"

        total_ht = round(state * prix_ht, 2)
        total_ttc = round(state * prix_ttc, 2)

        if inclure_abonnement and tarifs.get("abonnement_annuel"):
            abonnement = float(tarifs.get("abonnement_annuel", 0))
            repartition = {"jour": 365, "semaine": 52, "mois": 12, "annee": 1}
            factor = repartition.get(periode, 12)
            total_ht += round(abonnement / factor, 2)
            total_ttc += round(abonnement * 1.2 / factor, 2)

        return {
            "entity_id": entity.get("entity_id", "inconnu"),
            "nom": entity.get("attributes", {}).get("friendly_name", entity.get("entity_id", "inconnu")),
            "energie_kwh": round(state, 2),
            "mode_tarif": mode,
            "total_ht": total_ht,
            "total_ttc": total_ttc
        }

    except Exception as e:
        print(f"⚠️ Ignoré {entity.get('entity_id', 'inconnu')} → {e}")
        return None