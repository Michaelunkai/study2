#!/usr/bin/env  

# Name: setup_nocodb.sh
# Description: Script to install NocoDB on Ubuntu
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
apt-get update && apt-get upgrade -y
apt-get install -y \
    curl \
    sudo \
    mc
msg_ok "Dependencies installed"

# Install NocoDB
msg_info "Installing NocoDB"
mkdir -p /opt/nocodb
cd /opt/nocodb
curl -s http://get.nocodb.com/linux-x64 -o nocodb -L
chmod +x nocodb
msg_ok "NocoDB installed"

# Create and enable NocoDB service
msg_info "Creating NocoDB service"
cat <<EOF >/etc/systemd/system/nocodb.service
[Unit]
Description=NocoDB

[Service]
Type=simple
Restart=always
User=root
WorkingDirectory=/opt/nocodb
ExecStart=/opt/nocodb/nocodb

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now nocodb.service
msg_ok "NocoDB service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "NocoDB installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "NocoDB is running and accessible at: http://$IP_ADDRESS:8080"
