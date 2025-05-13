#!/usr/bin/env  

# Name: setup_readeck.sh
# Description: Script to install Readeck on Ubuntu
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

# Install Readeck
msg_info "Installing Readeck"
LATEST=$(curl -s https://codeberg.org/readeck/readeck/releases/ | grep -oP '(?<=Version )\d+\.\d+\.\d+' | head -1)
mkdir -p /opt/readeck
cd /opt/readeck
wget -q -O readeck https://codeberg.org/readeck/readeck/releases/download/${LATEST}/readeck-${LATEST}-linux-amd64
chmod a+x readeck
msg_ok "Readeck installed"

# Create and enable Readeck service
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/readeck.service
[Unit]
Description=Readeck Service
After=network.target

[Service]
Environment=READECK_SERVER_HOST=0.0.0.0
Environment=READECK_SERVER_PORT=8000
ExecStart=/opt/readeck/readeck serve
WorkingDirectory=/opt/readeck
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now readeck.service
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Readeck installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Readeck is running and accessible at: http://$IP_ADDRESS:8000"
