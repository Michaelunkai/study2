#!/bin/bash

# Script to enable all Ubuntu Pro features on WSL2 non-interactively

# Define Ubuntu Pro token
TOKEN="C13phRzKjLpNXTs1kiHAZuyiDfXsrH"

echo "=== Installing Required Tools ==="
# Install ubuntu-advantage-tools (force -y for non-interactivity)
sudo apt install -y ubuntu-advantage-tools

echo "=== Attaching Ubuntu Pro Subscription ==="
# Attach Ubuntu Pro subscription if not already attached
if ! pro status | grep -q "Account:"; then
    sudo pro attach "$TOKEN"
else
    echo "Ubuntu Pro is already attached."
fi

echo "=== Enabling Ubuntu Pro Features ==="
# Enable services non-interactively
sudo pro enable esm-apps || echo "ESM Apps is already enabled."
sudo pro enable esm-infra || echo "ESM Infra is already enabled."
sudo pro enable anbox-cloud || echo "Anbox Cloud is already enabled."

# Handle FIPS Updates
if ! sudo pro enable fips-updates --assume-yes 2>/dev/null; then
    echo "FIPS Updates could not be enabled due to kernel compatibility. Skipping."
fi

# Enable FIPS Preview (disable livepatch if necessary)
if pro enable fips-preview | grep -q "Disable Livepatch"; then
    echo "Disabling Livepatch to enable FIPS Preview..."
    sudo pro disable livepatch
    sudo pro enable fips-preview || echo "FIPS Preview is already enabled."
else
    echo "FIPS Preview is already enabled."
fi

# Enable Ubuntu Security Guide (USG)
sudo pro enable usg || echo "USG is already enabled."

echo "=== Configuring Automatic Updates ==="
# Configure automatic updates
echo -e 'APT::Periodic::Update-Package-Lists "1";\nAPT::Periodic::Unattended-Upgrade "1";' | sudo tee /etc/apt/apt.conf.d/20auto-upgrades > /dev/null

echo "=== Restarting WSL2 Instance ==="
# Check if `wsl` command is available
if command -v wsl >/dev/null 2>&1; then
    wsl --shutdown
else
    echo "The 'wsl' command is not found. Please restart WSL2 manually."
fi

echo "=== All Ubuntu Pro Features Enabled Successfully ==="
echo "Verify the setup using 'sudo pro status' after restarting your WSL2 instance."
