#!/usr/bin/env  

# Name: setup_watchyourlan.sh
# Description: Script to install WatchYourLAN on Ubuntu
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
    mc \
    gpg \
    arp-scan \
    ieee-data \
    libwww-perl
msg_ok "Dependencies installed"

# Install WatchYourLAN
msg_info "Installing WatchYourLAN"
RELEASE=$(curl -s https://api.github.com/repos/aceberg/WatchYourLAN/releases/latest | grep -o '"tag_name": *"[^"]*"' | cut -d '"' -f 4)
wget -q https://github.com/aceberg/WatchYourLAN/releases/download/$RELEASE/watchyourlan_${RELEASE}_linux_amd64.deb
dpkg -i watchyourlan_${RELEASE}_linux_amd64.deb
rm watchyourlan_${RELEASE}_linux_amd64.deb

# Create configuration file
mkdir -p /data
cat <<EOF >/data/config. 
arp_timeout: "500"
auth: false
auth_expire: 7d
auth_password: ""
auth_user: ""
color: dark
dbpath: /data/db. ite
guiip: 0.0.0.0
guiport: "8840"
history_days: "30"
iface: eth0
ignoreip: "no"
loglevel: verbose
shoutrrr_url: ""
theme: solar
timeout: 60
EOF
msg_ok "Installed WatchYourLAN"

# Create and configure the systemd service
msg_info "Creating Service"
sed -i 's|/etc/watchyourlan/config.yaml|/data/config.yaml|' /lib/systemd/system/watchyourlan.service
systemctl enable --now watchyourlan.service
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "WatchYourLAN installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "WatchYourLAN is running and accessible at: http://$IP_ADDRESS:8840"
echo ""
echo "### WatchYourLAN: Local Network Monitoring Tool"
echo "Monitor devices on your network with a clean, configurable web interface."
