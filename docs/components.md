# 🔧 Composants principaux de l’intégration `suivi_elec`

Ce document décrit les fichiers centraux de l’intégration Home Assistant `suivi_elec`, leur rôle fonctionnel, et leurs interactions.

---

## 📂 Fichiers racine de l’intégration

| Fichier            | Rôle principal                                         | Dépendances clés                  | Statut        |
|--------------------|--------------------------------------------------------|-----------------------------------|---------------|
| `__init__.py`      | Point d’entrée de l’intégration HA                     | `launcher.run_all()`              | ✅ Utilisé     |
| `manifest.json`    | Métadonnées HA (nom, version, dépendances, fichiers)  | Références aux fichiers et libs   | ✅ Utilisé     |
| `launcher.py`      | Lancement des routines principales                     | `helpers.loader`, `detect.py`     | ✅ Utilisé     |
| `generator.py`     | Génération d’entités HA                                | `helpers.regroupement`, `install_helper`, `loader` | ✅ Utilisé     |
| `translations/fr.json` | Traductions pour l’interface HA                   | Clés utilisées dans `manifest.json` | ✅ Utilisé     |

---

## 🧠 Modules utilitaires (helpers)

Les modules du dossier `helpers/` sont documentés séparément dans [`docs/helpers.md`](helpers.md).

---

## ⚙️ Automatisation & maintenance

| Fichier                  | Rôle | Statut |
|--------------------------|------|--------|
| `.github/workflows/release.yml` | Automatisation des releases via GitHub Actions | ✅ Utilisé |
| `update_git.sh`          | Script local de mise à jour du dépôt | ❓ À confirmer |

---

## 📌 Notes

- Tous les composants listés ici sont actifs dans le cycle de vie de l’intégration.
- Les dépendances sont internes (entre fichiers) ou externes (Home Assistant, API).
- Pour les modules secondaires, voir [`docs/helpers.md`](helpers.md).

---

*Dernière mise à jour : 10 septembre 2025*