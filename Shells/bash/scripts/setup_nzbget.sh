#!/usr/bin/env  

# Name: setup_nzbget.sh
# Description: Script to install NZBGet on Debian-based systems
# Author: tteck
# Co-Author: havardthom
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
    par2

cat <<EOF >/etc/apt/sources.list.d/non-free.list
deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
EOF

apt-get update && apt-get install -y unrar
rm /etc/apt/sources.list.d/non-free.list
msg_ok "Dependencies installed"

# Install NZBGet
msg_info "Installing NZBGet"
mkdir -p /etc/apt/keyrings
curl -fsSL https://nzbgetcom.github.io/nzbgetcom.asc | gpg --dearmor -o /etc/apt/keyrings/nzbgetcom.gpg
echo "deb [signed-by=/etc/apt/keyrings/nzbgetcom.gpg] https://nzbgetcom.github.io/deb stable main" >/etc/apt/sources.list.d/nzbgetcom.list
apt-get update && apt-get install -y nzbget
msg_ok "NZBGet installed"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL, username, and password
msg_info "NZBGet installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
USERNAME="nzbget"
PASSWORD="nzbget"
echo -e "NZBGet is running and accessible at: \033[1;32mhttp://$IP_ADDRESS:6789\033[0m"
echo -e "Username: \033[1;32m$USERNAME\033[0m"
echo -e "Password: \033[1;32m$PASSWORD\033[0m"
