#!/usr/bin/env  

# Name: setup_homebridge.sh
# Description: Script to install Homebridge on Ubuntu 22 WSL2
# Author: Adapted for WSL2 by Assistant
# License: MIT

# Exit on any error
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

# Update and install dependencies
msg_info "Updating system and installing dependencies"
apt-get update && apt-get upgrade -y
apt-get install -y curl sudo mc avahi-daemon gnupg2
msg_ok "System updated and dependencies installed"

# Set up Homebridge repository
msg_info "Setting up Homebridge repository"
curl -sSf https://repo.homebridge.io/KEY.gpg | gpg --dearmor >/usr/share/keyrings/homebridge.gpg
echo 'deb [signed-by=/usr/share/keyrings/homebridge.gpg] https://repo.homebridge.io stable main' >/etc/apt/sources.list.d/homebridge.list
apt-get update
msg_ok "Homebridge repository set up"

# Install Homebridge
msg_info "Installing Homebridge"
apt-get install -y homebridge
msg_ok "Homebridge installed"

# Cleanup
msg_info "Cleaning up"
apt-get -y autoremove && apt-get -y autoclean
msg_ok "System cleanup complete"

# Start Homebridge and echo the URL
msg_info "Starting Homebridge"
systemctl start homebridge
msg_ok "Homebridge started"

# Display Web UI URL
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Homebridge Web UI is accessible at: http://$IP_ADDRESS:8581"
