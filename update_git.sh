#!/bin/bash

DATE_TAG=$(date +"v%Y.%m.%d-%H%M")
MESSAGE="Auto release $DATE_TAG"

echo "📦 Commit + tag : $DATE_TAG"
git add .
git commit -m "$MESSAGE"
git tag "$DATE_TAG"
git push origin dev
git push origin "$DATE_TAG"

echo "✅ Release auto déclenchée via GitHub Actions"