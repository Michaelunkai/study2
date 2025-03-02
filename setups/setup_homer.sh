#!/usr/bin/env  

# Name: setup_homer.sh
# Description: Script to install Homer Dashboard on Ubuntu 22 WSL2
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
apt-get install -y curl sudo mc python3 python3-pip unzip
msg_ok "Dependencies installed"

# Install Homer Dashboard
msg_info "Installing Homer Dashboard"
mkdir -p /opt/homer
cd /opt/homer
wget -q https://github.com/bastienwirtz/homer/releases/latest/download/homer.zip
unzip -q homer.zip
rm -f homer.zip
cp assets/config.yml.dist assets/config.yml
msg_ok "Homer Dashboard installed"

# Create and enable service
msg_info "Creating Homer service"
cat <<EOF >/etc/systemd/system/homer.service
[Unit]
Description=Homer Dashboard Service
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/opt/homer
ExecStart=/usr/bin/python3 -m http.server 8010
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now homer.service
msg_ok "Homer service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display success message
msg_info "Homer Dashboard installation complete"
echo "Homer Dashboard is accessible at: http://$(hostname -I | awk '{print $1}'):8010"
