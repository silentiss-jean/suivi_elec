import os
import importlib.util
import logging

_LOGGER = logging.getLogger(__name__)

def charger_groupes(nom_module, hass=None):
    dossier = os.path.dirname(os.path.dirname(__file__))
    chemin = os.path.join(dossier, f"{nom_module}.py")

    if not os.path.exists(chemin):
        _LOGGER.warning(f"[suivi_elec] ⚠️ Fichier {chemin} introuvable.")
        return []

    try:
        spec = importlib.util.spec_from_file_location(nom_module, chemin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        groupes = getattr(module, "groupes", None)
        if not isinstance(groupes, list):
            _LOGGER.error(f"[suivi_elec] ❌ 'groupes' doit être une liste, pas {type(groupes)}.")
            return []

        groupes_valides = []
        for i, groupe in enumerate(groupes):
            if not isinstance(groupe, dict):
                _LOGGER.warning(f"[suivi_elec] Groupe #{i} ignoré : type invalide.")
                continue

            nom = groupe.get("nom")
            capteurs = groupe.get("capteurs")

            if not isinstance(nom, str) or not isinstance(capteurs, list):
                _LOGGER.warning(f"[suivi_elec] Groupe mal formé : {groupe}")
                continue

            capteurs_valides = [
                c for c in capteurs
                if isinstance(c, str) and (not hass or c in hass.states.async_entity_ids())
            ]

            if capteurs_valides:
                groupes_valides.append({"nom": nom, "capteurs": capteurs_valides})
            else:
                _LOGGER.warning(f"[suivi_elec] Aucun capteur valide pour le groupe '{nom}'.")

        return groupes_valides

    except Exception as e:
        _LOGGER.error(f"[suivi_elec] ❌ Erreur lors du chargement : {e}")
        return []