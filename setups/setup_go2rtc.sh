#!/usr/bin/env  

# Name: setup_go2rtc.sh
# Description: Script to install go2rtc on Ubuntu 22 WSL2
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
apt-get install -y curl sudo mc
msg_ok "Dependencies installed"

# Install go2rtc
msg_info "Installing go2rtc"
mkdir -p /opt/go2rtc
cd /opt/go2rtc
wget -q https://github.com/AlexxIT/go2rtc/releases/latest/download/go2rtc_linux_amd64
chmod +x go2rtc_linux_amd64
msg_ok "go2rtc installed"

# Create and enable go2rtc service
msg_info "Creating go2rtc service"
cat <<EOF >/etc/systemd/system/go2rtc.service
[Unit]
Description=go2rtc Streaming Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/opt/go2rtc/go2rtc_linux_amd64
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now go2rtc.service
msg_ok "go2rtc service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display success message
msg_info "go2rtc installation complete"
echo "go2rtc is running. Access it at http://$(hostname -I | awk '{print $1}'):1984"
