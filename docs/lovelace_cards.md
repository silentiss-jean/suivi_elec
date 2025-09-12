# 📊 Exemples de cartes Lovelace — Intégration `suivi_elec`

Ce fichier regroupe des exemples de cartes Lovelace pour visualiser les entités générées par l'intégration `suivi_elec`. Tu peux enrichir ce fichier au fur et à mesure avec d'autres vues, capteurs ou résumés.

---

## 🧩 Carte 1 — Statut de l'intégration

```yaml
type: entities
title: 🔌 Suivi Élec — Statut
entities:
  - entity: sensor.suivi_elec_status
    name: Mode & Entités
  - type: attribute
    entity: sensor.suivi_elec_status
    attribute: mode
    name: Mode actif
  - type: attribute
    entity: sensor.suivi_elec_status
    attribute: entites_actives
    name: Entités activées
  - type: attribute
    entity: sensor.suivi_elec_status
    attribute: source
    name: Source API / Instance
✅ Résultat attendu

Affiche :

•  Le mode actif (local ou cloud)
•  Le nombre d'entités activées
•  L'URL source utilisée
📁 Emplacement

Ce fichier est situé dans :
/config/suivi_elec/docs/lovelace_cards.md
/config/suivi_elec/docs/lovelace_cards.md
Tu peux lier ce fichier depuis ton docs/README.md ou l'intégrer dans ton dépôt Git pour le suivi collaboratif.

---

## 🧩 Carte 2 — Entités activées dynamiquement

```yaml
type: entities
title: ⚡ Suivi Élec — Entités activées
entities:
  - entity: sensor.suivi_elec_conso_jour
    name: Consommation journalière
    icon: mdi:flash
  - entity: sensor.suivi_elec_cout_jour
    name: Coût journalier
    icon: mdi:currency-eur
  - entity: sensor.suivi_elec_conso_mois
    name: Consommation mensuelle
    icon: mdi:calendar-month
  - entity: sensor.suivi_elec_cout_mois
    name: Coût mensuel
    icon: mdi:currency-eur
🧠 Notes

•  Cette carte suppose que les entités listées ont été activées via options_flow
•  Tu peux adapter dynamiquement cette carte en fonction des entités réellement créées
•  Les icônes mdi: sont personnalisables selon le type d’information affichée
📁 Emplacement

Ce bloc est ajouté dans :
/config/suivi_elec/docs/lovelace_cards.md
Tu peux enrichir ce fichier avec :

•  Des cartes graphiques (type: gauge, type: statistics-graph)
•  Des vues par résidence ou par profil utilisateur
•  Des résumés hebdomadaires ou comparatifs
