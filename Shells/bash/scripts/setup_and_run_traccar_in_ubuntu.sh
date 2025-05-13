#!/usr/bin/env  

# Name: setup_traccar.sh
# Description: Script to install Traccar on Ubuntu
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
apt-get update && apt-get upgrade -y
apt-get install -y \
    curl \
    sudo \
    mc
msg_ok "Dependencies installed"

# Get the latest release of Traccar
RELEASE=$(curl -s https://api.github.com/repos/traccar/traccar/releases/latest | grep "tag_name" | awk '{print substr($2, 3, length($2)-4) }')
msg_info "Installing Traccar v${RELEASE}"
wget -q https://github.com/traccar/traccar/releases/download/v${RELEASE}/traccar-linux-64-${RELEASE}.zip
unzip traccar-linux-64-${RELEASE}.zip
./traccar.run

# Enable and start Traccar service
systemctl enable --now traccar
rm -rf README.txt traccar-linux-64-${RELEASE}.zip traccar.run
msg_ok "Installed Traccar v${RELEASE}"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Traccar installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Traccar is running and accessible at: http://$IP_ADDRESS:8082"
echo ""
echo "### Traccar: Real-Time GPS Tracking"
echo "A powerful tool for monitoring and managing GPS tracking data."
