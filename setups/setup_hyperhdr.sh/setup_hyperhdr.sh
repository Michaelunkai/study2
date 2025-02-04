#!/usr/bin/env  

# Name: setup_hyperhdr.sh
# Description: Script to install HyperHDR on Ubuntu 22 WSL2
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
apt-get install -y curl sudo mc gpg
msg_ok "Dependencies installed"

# Install HyperHDR
msg_info "Installing HyperHDR"
curl -fsSL https://awawa-dev.github.io/hyperhdr.public.apt.gpg.key >/usr/share/keyrings/hyperhdr.public.apt.gpg.key
chmod go+r /usr/share/keyrings/hyperhdr.public.apt.gpg.key
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hyperhdr.public.apt.gpg.key] https://awawa-dev.github.io $(awk -F= '/VERSION_CODENAME/ {print $2}' /etc/os-release) main" >/etc/apt/sources.list.d/hyperhdr.list
apt-get update
apt-get install -y hyperhdr
msg_ok "HyperHDR installed"

# Create and enable the service
msg_info "Creating and enabling HyperHDR service"
cat <<EOF >/etc/systemd/system/hyperhdr.service
[Unit]
Description=HyperHDR Service
After=syslog.target network.target

[Service]
Restart=on-failure
RestartSec=5
Type=simple
ExecStart=/usr/bin/hyperhdr

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now hyperhdr
msg_ok "HyperHDR service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message
msg_info "HyperHDR installation complete"
echo "HyperHDR is now installed and running. You can manage it using the HyperHDR service."
