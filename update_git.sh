
cer dans le dossier du projet
cd "$(dirname "$0")"

# 🔐 Vérifie que le fichier .env existe
if [ ! -f .env ]; then
  echo "❌ Fichier .env introuvable. Création..."
  read -p "➡️  Entrez l'URL de Home Assistant (ex: http://192.168.3.160:8123) : " HA_URL
  read -p "➡️  Entrez ton nouveau token Home Assistant : " HA_TOKEN
  echo "HA_URL=$HA_URL" > .env
  echo "HA_TOKEN=$HA_TOKEN" >> .env
  echo ".env" >> .gitignore
  echo "✅ Fichier .env créé et sécurisé."
fi

# 🧼 Nettoyer les fichiers compilés
find . -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -delete

# 📦 Ajouter les fichiers modifiés
git add custom_components/suivi_elec/helpers/detect.py .gitignore

# 🔍 Détection des fichiers non trackés
UNTRACKED=$(git ls-files --others --exclude-standard)

if [ -n "$UNTRACKED" ]; then
  echo "⚠️ Fichiers non trackés détectés :"
  echo "$UNTRACKED"
  read -p "❓ Souhaites-tu les inclure dans le commit ? (yes/no) : " INCLUDE
  if [ "$INCLUDE" = "yes" ]; then
    echo "$UNTRACKED" | xargs git add
    echo "✅ Fichiers ajoutés au commit."
  else
    echo "⏹️ Fichiers non ajoutés."
  fi
fi

# 📝 Commit avec message clair
git commit -m "🔐 Mise à jour sécurisée + détection automatique des fichiers non trackés"

# 🏷️ Créer un tag versionné basé sur la date
TAG="v$(date +%Y.%m.%d-%H%M)"
git tag "$TAG"

# 🚀 Pousser vers GitHub
git push origin dev
git push origin "$TAG"

echo "✅ Mise à jour publiée avec succès : $TAG"
