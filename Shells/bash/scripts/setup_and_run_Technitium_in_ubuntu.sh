#!/usr/bin/env  

# Name: setup_technitium_dns.sh
# Description: Script to install Technitium DNS on Ubuntu
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

# Install ASP.NET Core Runtime
msg_info "Installing ASP.NET Core Runtime"
wget -q https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
dpkg -i packages-microsoft-prod.deb
rm -rf packages-microsoft-prod.deb
apt-get update
apt-get install -y aspnetcore-runtime-8.0
msg_ok "ASP.NET Core Runtime installed"

# Install Technitium DNS
msg_info "Installing Technitium DNS"
bash <(curl -fsSL https://download.technitium.com/dns/install.sh)
msg_ok "Technitium DNS installed"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Technitium DNS installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Technitium DNS is running and accessible at: http://$IP_ADDRESS:5380"
echo ""
echo "### Technitium DNS: Custom DNS Server"
echo "An advanced, privacy-focused, and configurable DNS server for managing local and public DNS records."
