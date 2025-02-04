#!/usr/bin/env  

# Name: setup_podman.sh
# Description: Script to install and configure Podman on Ubuntu
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
apt-get update && apt-get install -y \
    curl \
    sudo \
    mc
msg_ok "Dependencies installed"

# Install Podman
msg_info "Installing Podman"
apt-get -y install podman
systemctl enable --now podman.socket
echo -e 'unqualified-search-registries=["docker.io"]' >> /etc/containers/registries.conf
msg_ok "Podman installed and configured"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message
msg_info "Podman installation complete"
echo "Podman is installed and ready to use. The Podman socket is enabled for container management."
