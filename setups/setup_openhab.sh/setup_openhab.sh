#!/usr/bin/env  

# Name: setup_openhab.sh
# Description: Script to install openHAB on Ubuntu
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
    gnupg \
    apt-transport-https
msg_ok "Dependencies installed"

# Install Azul Zulu (Java 17)
msg_info "Installing Azul Zulu"
wget -qO /etc/apt/trusted.gpg.d/zulu-repo.asc "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xB1998361219BD9C9"
wget -q https://cdn.azul.com/zulu/bin/zulu-repo_1.0.0-3_all.deb
dpkg -i zulu-repo_1.0.0-3_all.deb
apt-get update
apt-get -y install zulu17-jdk
msg_ok "Azul Zulu installed"

# Install openHAB
msg_info "Installing openHAB"
curl -fsSL "https://openhab.jfrog.io/artifactory/api/gpg/key/public" | gpg --dearmor >openhab.gpg
mv openhab.gpg /usr/share/keyrings
chmod u=rw,g=r,o=r /usr/share/keyrings/openhab.gpg
echo "deb [signed-by=/usr/share/keyrings/openhab.gpg] https://openhab.jfrog.io/artifactory/openhab-linuxpkg stable main" >/etc/apt/sources.list.d/openhab.list
apt update
apt-get -y install openhab
systemctl daemon-reload
systemctl enable --now openhab.service
msg_ok "openHAB installed"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "openHAB installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo -e "openHAB is running and accessible at:"
echo -e "  Web UI: \033[1;32mhttp://$IP_ADDRESS:8080\033[0m"
echo -e "  Console: \033[1;32mhttp://$IP_ADDRESS:9001\033[0m (optional)"
