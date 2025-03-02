#!/usr/bin/env  

# Name: setup_transmission.sh
# Description: Script to install Transmission on Ubuntu
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
msg_info "Installing Dependencies"
apt-get update && apt-get upgrade -y
apt-get install -y \
    curl \
    sudo \
    mc
msg_ok "Dependencies installed"

# Install Transmission
msg_info "Installing Transmission"
apt-get install -y transmission-daemon
systemctl stop transmission-daemon

# Configure Transmission
sed -i 's/"rpc-whitelist-enabled": true/"rpc-whitelist-enabled": false/g' /etc/transmission-daemon/settings.json
sed -i 's/"rpc-host-whitelist-enabled": true/"rpc-host-whitelist-enabled": false/g' /etc/transmission-daemon/settings.json

systemctl start transmission-daemon
msg_ok "Transmission installed and configured"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Transmission installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Transmission is running and accessible at: http://$IP_ADDRESS:9091"
echo ""
echo "### Transmission: Lightweight Torrent Client"
echo "A fast, easy, and open-source BitTorrent client with a web interface."
