#!/usr/bin/env  

# Name: setup_thelounge.sh
# Description: Script to install The Lounge on Ubuntu
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
apt-get update && apt-get upgrade -y
apt-get install -y \
    curl \
    gpg \
    wget \
    mc
msg_ok "Dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js Repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
apt-get update
msg_ok "Node.js Repository set up"

# Install Node.js and Yarn
msg_info "Installing Node.js"
apt-get install -y nodejs
npm install --global yarn
msg_ok "Node.js installed"

# Install The Lounge
msg_info "Installing The Lounge"
cd /opt
RELEASE=$(curl -s https://api.github.com/repos/thelounge/thelounge-deb/releases/latest | grep "tag_name" | awk '{print substr($2, 3, length($2)-4) }')
wget -q https://github.com/thelounge/thelounge-deb/releases/download/v${RELEASE}/thelounge_${RELEASE}_all.deb
dpkg -i ./thelounge_${RELEASE}_all.deb
echo "${RELEASE}" >"/opt/thelounge_version.txt"
msg_ok "The Lounge installed"

# Cleanup
msg_info "Cleaning up"
rm -rf /opt/thelounge_${RELEASE}_all.deb
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "The Lounge installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "The Lounge is running and accessible at: http://$IP_ADDRESS:9000"
echo ""
echo "### The Lounge: Accessible IRC Client"
echo "A modern, responsive, and always-online web IRC client for managing chat conversations."
