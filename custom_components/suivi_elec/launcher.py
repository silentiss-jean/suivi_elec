from helpers.detect import detect_capteurs
from helpers.regroupement import regroupe_capteurs
from helpers.generation import generate_all

def run_all():
    print("🔍 Étape 1 : Détection des capteurs...")
    detect_capteurs()

    print("📦 Étape 2 : Regroupement par pièce (automatique + personnalisé)...")
    regroupe_capteurs()

    print("⚡ Étape 3 : Génération des fichiers YAML et Lovelace...")
    generate_all()

    print("✅ Tous les fichiers ont été générés avec succès.")