# PowerShell deployment script for GitHub Pages

Write-Host "Building the project..." -ForegroundColor Green
Set-Location frontend
npm run build

Write-Host "Deploying to gh-pages branch..." -ForegroundColor Green
Set-Location dist

# Initialize git in dist folder
Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
git init
git checkout -b main

# Add .nojekyll file to bypass Jekyll processing
New-Item -ItemType File -Path ".nojekyll" -Force | Out-Null

git add -A
git commit -m "deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

# Push to gh-pages branch
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -f git@github.com-personal:Naveenasri-T/Done-List.git main:gh-pages

Set-Location ../..
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "Your site will be available at: https://naveenasri-t.github.io/Done-List/" -ForegroundColor Cyan
