# PowerShell script to automate VS Code + Copilot environment setup

# Install VS Code extensions
code --install-extension github.copilot
code --install-extension github.copilot-chat

# Optional: Install Python extension if needed
# code --install-extension ms-python.python

# Print success message
Write-Host "VS Code Copilot environment setup complete."
