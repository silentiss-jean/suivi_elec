# 🗺️ Roadmap – Suivi Élec

Ce document présente les orientations futures du projet `suivi_elec`, les fonctionnalités envisagées, les améliorations techniques et les objectifs communautaires.

---

## ✅ Objectifs atteints

- [x] Mise en place d’une structure modulaire (`helpers/`, `launcher.py`, etc.)
- [x] Automatisation des releases via GitHub Actions
- [x] Documentation technique complète (`docs/`)
- [x] Nettoyage des modules inutilisés
- [x] Traductions françaises intégrées

---

## 🟡 Prochaines étapes (court terme)

- [ ] Ajouter une interface de configuration via l’UI Home Assistant
- [ ] Créer des sensors HA dynamiques à partir des données API
- [ ] Intégrer un fallback local en cas d’échec de l’API
- [ ] Ajouter des tests unitaires pour `detect.py`, `calculateur.py`, etc.
- [ ] Créer un badge HACS pour faciliter l’intégration

---

## 🔵 Évolutions envisagées (moyen terme)

- [ ] Support multi-fournisseurs (ex. Engie, TotalEnergies)
- [ ] Ajout d’un mode “simulation tarifaire” pour comparer les offres
- [ ] Export des données vers CSV ou Grafana via MQTT
- [ ] Intégration avec le système de notification HA (`persistent_notification`)
- [ ] Ajout d’un mode debug visuel pour les entités détectées

---

## 🟣 Vision long terme

- [ ] Interface web dédiée (dashboard externe)
- [ ] API REST locale pour exposer les données
- [ ] Système de plugins pour étendre les calculs ou les sources
- [ ] Traductions multilingues (EN, ES, DE)
- [ ] Publication sur le store officiel Home Assistant (si éligible)

---

## 🤝 Contributions bienvenues

Tu peux participer à l’évolution du projet en proposant :

- Des idées ou fonctionnalités
- Des corrections de bugs
- Des améliorations de performance
- Des traductions
- Des tests automatisés

---

*Dernière mise à jour : 10 septembre 2025*