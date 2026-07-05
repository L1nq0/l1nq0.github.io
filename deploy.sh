#!/bin/bash
set -e

echo "[1/3] Building Hugo site..."
hugo --cleanDestinationDir

echo "[2/3] Preparing deployment..."
# Clean leftover .git from previous deployment (hugo does not remove it)
rm -rf public/.git
cd public

git init
git checkout -b main
git add -A
git commit -m "deploy: $(date '+%Y-%m-%d %H:%M:%S')"

echo "[3/3] Pushing to GitHub Pages..."
git remote add origin https://github.com/L1nq0/L1nq0.github.io.git
git push -f origin main

cd ..
echo ""
echo "Deployment complete. Site available at https://sw1mblu3.fun/"
echo "It may take 1-2 minutes for GitHub Pages to reflect changes."
