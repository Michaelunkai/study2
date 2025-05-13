#!/usr/bin/env  

# Name: setup_gotify.sh
# Description: Script to install Gotify on Ubuntu 22 WSL2
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
apt-get install -y curl sudo mc unzip
msg_ok "Dependencies installed"

# Install Gotify
msg_info "Installing Gotify"
RELEASE=$(curl -s https://api.github.com/repos/gotify/server/releases/latest | grep "tag_name" | awk -F '"' '{print $4}')
mkdir -p /opt/gotify
cd /opt/gotify
wget -q https://github.com/gotify/server/releases/download/v${RELEASE}/gotify-linux-amd64.zip
unzip -q gotify-linux-amd64.zip
rm -f gotify-linux-amd64.zip
chmod +x gotify-linux-amd64
echo "${RELEASE}" > /opt/gotify_version.txt
msg_ok "Gotify installed"

# Create and enable Gotify service
msg_info "Creating Gotify service"
cat <<EOF >/etc/systemd/system/gotify.service
[Unit]
Description=Gotify Notification Server
Requires=network.target
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/gotify
ExecStart=/opt/gotify/gotify-linux-amd64
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now gotify.service
msg_ok "Gotify service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display success message
msg_info "Gotify installation complete"
echo "Gotify is running and accessible on port 80. Configure further settings in /opt/gotify/config.yml."
