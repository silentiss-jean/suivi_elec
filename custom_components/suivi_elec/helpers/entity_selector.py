def comparer_entites(detectees: list, potentielles: list) -> dict:
    """
    Compare les entités détectées avec celles que l'intégration peut créer.
    Retourne un dictionnaire avec :
    - existantes : déjà présentes dans HA
    - nouvelles : à créer
    - toutes : vue globale
    """
    detectee_ids = [e["entity_id"] for e in detectees]
    existantes = [e for e in potentielles if e in detectee_ids]
    nouvelles = [e for e in potentielles if e not in detectee_ids]

    return {
        "existantes": existantes,
        "nouvelles": nouvelles,
        "toutes": potentielles
    }