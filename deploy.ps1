# Hugo Blog Deployment Script (PowerShell)
# Builds Hugo site and deploys to GitHub Pages

$ErrorActionPreference = "Stop"

Write-Host "[1/3] Building Hugo site..." -ForegroundColor Cyan
hugo --cleanDestinationDir --buildFuture
if ($LASTEXITCODE -ne 0) { throw "Hugo build failed" }

Write-Host "[2/3] Preparing deployment..." -ForegroundColor Cyan

# Clean leftover .git from previous deployment (hugo does not remove it)
Remove-Item -Recurse -Force public/.git -ErrorAction SilentlyContinue

Push-Location public

git init
git checkout -b main
git add -A
$commitMsg = "deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git commit -m $commitMsg

Write-Host "[3/3] Pushing to GitHub Pages..." -ForegroundColor Cyan
git remote add origin https://github.com/L1nq0/L1nq0.github.io.git
git push -f origin main

Pop-Location

Write-Host ""
Write-Host "Deployment complete. Site: https://sw1mblu3.fun/" -ForegroundColor Green
Write-Host "It may take 1-2 minutes for GitHub Pages to reflect changes."
