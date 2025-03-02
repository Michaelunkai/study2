#!/usr/bin/env  

# Name: setup_meshcentral.sh
# Description: Script to install MeshCentral on Ubuntu
# Author: tteck (tteckster)
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
apt-get update && apt-get upgrade -y
apt-get install -y \
    curl \
    sudo \
    mc \
    ca-certificates \
    gnupg
msg_ok "Dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
apt-get update
msg_ok "Node.js repository set up"

# Install Node.js
msg_info "Installing Node.js"
apt-get install -y nodejs
msg_ok "Node.js installed"

# Install MeshCentral
msg_info "Installing MeshCentral"
mkdir -p /opt/meshcentral
cd /opt/meshcentral
npm install meshcentral
node node_modules/meshcentral --install
msg_ok "MeshCentral installed"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "MeshCentral installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "MeshCentral is running and accessible at: https://$IP_ADDRESS:443"
