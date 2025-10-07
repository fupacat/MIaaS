# PowerShell script to automate VS Code + Copilot environment setup

# Install VS Code extensions
code --install-extension github.copilot
code --install-extension github.copilot-chat

# Optional: Install Python extension if needed
# code --install-extension ms-python.python


# Git and GitHub automation
$repoName = Read-Host "Enter GitHub repo name (e.g. MIaaS)"
$repoOwner = Read-Host "Enter GitHub username/owner (e.g. fupacat)"
$userName = git config --global --get user.name
$userEmail = git config --global --get user.email
if (-not $userName) {
	$userName = Read-Host "Enter your git user.name"
	git config --global user.name $userName
}
if (-not $userEmail) {
	$userEmail = Read-Host "Enter your git user.email"
	git config --global user.email $userEmail
}
if (-not (Test-Path ".git")) {
	git init
}
git add .
git commit -m "Initial commit for $repoName environment automation"
gh repo create "$repoOwner/$repoName" --public --source . --remote origin --push

Write-Host "VS Code Copilot and GitHub environment setup complete."
