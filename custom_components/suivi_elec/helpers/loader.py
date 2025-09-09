import os
import importlib.util

def charger_groupes(nom_module):
    """
    Importe dynamiquement le fichier de groupes généré.
    Args:
        nom_module (str): Nom du fichier sans extension (ex: 'groupes_capteurs_energy')
    Returns:
        dict: Dictionnaire 'groupes' défini dans le module
    """
    dossier = os.path.dirname(os.path.dirname(__file__))  # remonte à suivi_elec/
    chemin = os.path.join(dossier, f"{nom_module}.py")

    if not os.path.exists(chemin):
        raise FileNotFoundError(f"❌ Fichier {chemin} introuvable.")

    spec = importlib.util.spec_from_file_location(nom_module, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "groupes"):
        raise AttributeError(f"❌ Le module {nom_module} ne contient pas de variable 'groupes'.")

    return module.groupes