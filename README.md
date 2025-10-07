# MIaaS - Model Infrastructure as a Service

MIaaS is an open platform for orchestrating AI/ML infrastructure across distributed nodes.

## 🚀 Quick Start

The MVP is ready to run! See [QUICKSTART.md](QUICKSTART.md) to run the control plane and agent in minutes.

## About This Project

This project uses VS Code and GitHub Copilot for AI-powered development. All environment setup is automated, including Git and GitHub integration.

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
- Initializes a git repository and configures your user info
- Creates a new GitHub repository and pushes the initial commit

## Manual Steps (if needed)
- Ensure you are using PowerShell 7+
- Check `.vscode/settings.json` for Copilot configuration
- If you want to use a different GitHub repo, update the script accordingly

## Troubleshooting
- If extension install fails, update VS Code and retry
- For more help, see the official Copilot docs
- If GitHub repo creation fails, check your authentication with `gh auth status`

## Project Documentation

- [QUICKSTART.md](QUICKSTART.md) - Run the MVP in minutes
- [MIaaS.md](MIaaS.md) - Full architecture and roadmap
- [Agent README](agent/README.md) - Agent documentation
- [Control Plane README](control-plane/README.md) - Control plane documentation
