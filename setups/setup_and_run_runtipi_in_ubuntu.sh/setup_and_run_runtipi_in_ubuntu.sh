#!/usr/bin/env  

# Name: setup_runtipi.sh
# Description: Script to install Runtipi on Ubuntu
# Author: tteck
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
    sudo \
    mc
msg_ok "Dependencies installed"

# Configure Docker logging
msg_info "Configuring Docker logging"
DOCKER_CONFIG_PATH='/etc/docker/daemon.json'
mkdir -p "$(dirname "$DOCKER_CONFIG_PATH")"
echo -e '{\n  "log-driver": "journald"\n}' > "$DOCKER_CONFIG_PATH"
systemctl restart docker
msg_ok "Docker logging configured"

# Install Runtipi
msg_info "Installing Runtipi (Patience)"
cd /opt
wget -q https://raw.githubusercontent.com/runtipi/runtipi/master/scripts/install.sh
chmod +x install.sh
./install.sh
chmod 666 /opt/runtipi/state/settings.json
msg_ok "Runtipi installed"

# Cleanup
msg_info "Cleaning up"
rm /opt/install.sh
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Runtipi installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Runtipi is installed and running."
echo "Access the Runtipi dashboard at: http://$IP_ADDRESS"
