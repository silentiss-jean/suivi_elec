import os
import yaml

def lire_configuration_yaml():
    """Lit le fichier configuration.yaml et retourne son contenu sous forme de dict."""
    chemin = "/config/configuration.yaml"
    if not os.path.exists(chemin):
        print("❌ Fichier configuration.yaml introuvable.")
        return {}

    try:
        with open(chemin, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config or {}
    except yaml.YAMLError as e:
        print(f"❌ Erreur de lecture YAML : {e}")
        return {}

def detecter_structure_packages(config):
    """Détecte la structure de configuration utilisée pour les packages."""
    homeassistant = config.get("homeassistant", {})
    packages = homeassistant.get("packages")

    if isinstance(packages, str) and "packages" in packages:
        return "dossier"
    elif isinstance(packages, dict):
        return "manuel"
    else:
        return "absent"

def choisir_emplacement_fichiers(mode_force=None, verbose=True):
    """
    Détermine où placer les fichiers générés selon la configuration.yaml.
    
    Args:
        mode_force (str): 'dossier', 'manuel' ou 'absent' pour forcer le mode
        verbose (bool): Affiche les messages d'information
    Returns:
        str: Chemin du dossier cible
    """
    if mode_force in ["dossier", "manuel", "absent"]:
        if mode_force == "dossier":
            dossier = "/config/packages/"
            if verbose:
                print("📦 Mode forcé : packages → fichiers placés dans /packages/")
        else:
            dossier = "/config/"
            if verbose:
                print(f"📄 Mode forcé : {mode_force} → fichiers placés à la racine")
                if mode_force == "absent":
                    print("👉 Pensez à ajouter dans configuration.yaml :")
                    print("homeassistant:\n  packages:\n    suivi_elec: !include suivi_elec.yaml")
        return dossier

    # Mode automatique
    config = lire_configuration_yaml()
    mode = detecter_structure_packages(config)

    if mode == "dossier":
        dossier = "/config/packages/"
        if verbose:
            print("📦 Mode packages détecté → fichiers placés dans /packages/")
    elif mode == "manuel":
        dossier = "/config/"
        if verbose:
            print("📄 Mode manuel détecté → fichiers placés à la racine")
    else:
        dossier = "/config/"
        if verbose:
            print("⚠️ Aucun package détecté → fichiers placés à la racine")
            print("👉 Pensez à ajouter dans configuration.yaml :")
            print("homeassistant:\n  packages:\n    suivi_elec: !include suivi_elec.yaml")

    return dossier