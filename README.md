# MIaaS Environment Setup

This project uses VS Code and GitHub Copilot for AI-powered development. Follow these steps to automate your local setup:

## Automated Setup

1. Open PowerShell in this directory.
2. Run the setup script:
   ```powershell
   ./setup.ps1
   ```
3. Open the project in VS Code:
   ```powershell
   code .
   ```

## What the Script Does
- Installs Copilot and Copilot Chat extensions for VS Code
- (Optional) Installs Python extension if uncommented
- Applies workspace settings for Copilot best practices

## Manual Steps (if needed)
- Ensure you are using PowerShell 7+
- Check `.vscode/settings.json` for Copilot configuration

## Troubleshooting
- If extension install fails, update VS Code and retry
- For more help, see the official Copilot docs
