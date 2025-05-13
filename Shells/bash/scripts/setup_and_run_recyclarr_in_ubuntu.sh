#!/usr/bin/env  

# Name: setup_recyclarr.sh
# Description: Script to install Recyclarr on Ubuntu
# Author: MrYadro
# License: MIT

# Exit immediately if a command exits with a non-zero status
set -e

# Functions for colored output
function msg_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

function msg_ok() {
    echo -e "\033[1;32m[OK]\033[0m $1"
}

function msg_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
    exit 1
}

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    msg_error "This script must be run as root or with sudo"
fi

# Install dependencies
msg_info "Installing dependencies"
apt-get update && apt-get install -y \
    curl \
    git \
    sudo \
    mc
msg_ok "Dependencies installed"

# Install Recyclarr
msg_info "Installing Recyclarr"
LATEST_RELEASE_URL=$(curl -s https://api.github.com/repos/recyclarr/recyclarr/releases/latest | grep download | grep linux-x64 | cut -d\" -f4)
wget -q "$LATEST_RELEASE_URL"
tar -C /usr/local/bin -xJf recyclarr*.tar.xz
mkdir -p /root/.config/recyclarr
recyclarr config create
msg_ok "Recyclarr installed"

# Cleanup
msg_info "Cleaning up"
rm -rf recyclarr*.tar.xz
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with configuration details
msg_info "Recyclarr installation complete"
echo "Recyclarr has been installed successfully."
echo "Configuration directory: /root/.config/recyclarr/"
echo "Use the following commands to manage Recyclarr:"
echo "  recyclarr config create     # Create a new configuration file"
echo "  recyclarr sync              # Sync configuration with your Radarr/Sonarr setup"
