#!/usr/bin/env  

# Name: setup_vikunja.sh
# Description: Script to install Vikunja on Ubuntu
# Author: MickLesk (Canbiz)
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
    make \
    mc
msg_ok "Dependencies installed"

# Install Vikunja
msg_info "Setting up Vikunja (Patience)"
cd /opt
RELEASE=$(curl -s https://dl.vikunja.io/vikunja/ | grep -oP 'href="/vikunja/\K[0-9]+\.[0-9]+\.[0-9]+' | sort -V | tail -n 1)
wget -q "https://dl.vikunja.io/vikunja/$RELEASE/vikunja-$RELEASE-amd64.deb"
dpkg -i vikunja-$RELEASE-amd64.deb

# Update configuration
sed -i 's|^  timezone: .*|  timezone: UTC|' /etc/vikunja/config.yml
sed -i 's|"./vikunja.db"|"/etc/vikunja/vikunja.db"|' /etc/vikunja/config.yml
sed -i 's|./files|/etc/vikunja/files|' /etc/vikunja/config.yml

# Start service
systemctl enable --now vikunja.service
echo "${RELEASE}" >/opt/vikunja_version.txt
msg_ok "Installed Vikunja"

# Cleanup
msg_info "Cleaning up"
rm -rf /opt/vikunja-$RELEASE-amd64.deb
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Vikunja installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Vikunja is running and accessible at: http://$IP_ADDRESS:3456"
echo ""
echo "### Vikunja: Open-Source Task Management"
echo "A powerful and flexible task management tool for individuals and teams."
