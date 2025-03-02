#!/usr/bin/env  

# Name: setup_onedev.sh
# Description: Script to install OneDev on Debian-based systems
# Author: kristocopani
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
    mc \
    sudo \
    default-jdk \
    git
msg_ok "Dependencies installed"

# Install OneDev
msg_info "Installing OneDev"
cd /opt
wget -q https://code.onedev.io/onedev/server/~site/onedev-latest.tar.gz
tar -xzf onedev-latest.tar.gz
mv /opt/onedev-latest /opt/onedev
/opt/onedev/bin/server.sh install
systemctl start onedev
RELEASE=$(grep "version" /opt/onedev/release.properties | cut -d'=' -f2)
echo "${RELEASE}" >/opt/onedev_version.txt
msg_ok "OneDev installed"

# Cleanup
msg_info "Cleaning up"
rm -rf /opt/onedev-latest.tar.gz
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "OneDev installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo -e "OneDev is running and accessible at:"
echo -e "  \033[1;32mhttp://$IP_ADDRESS:6610\033[0m"
