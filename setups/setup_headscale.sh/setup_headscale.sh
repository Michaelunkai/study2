#!/usr/bin/env  

# Name: setup_headscale.sh
# Description: Script to install Headscale on Ubuntu 22 WSL2
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

# Fetch the latest Headscale release
msg_info "Fetching the latest Headscale release"
RELEASE=$(curl -s https://api.github.com/repos/juanfont/headscale/releases/latest | grep "tag_name" | awk -F '"' '{print $4}')
msg_info "Installing Headscale v${RELEASE}"
wget -q https://github.com/juanfont/headscale/releases/download/v${RELEASE}/headscale_${RELEASE}_linux_amd64.deb

# Install Headscale
dpkg -i headscale_${RELEASE}_linux_amd64.deb
systemctl enable --now headscale
echo "${RELEASE}" > /opt/headscale_version.txt
msg_ok "Installed Headscale v${RELEASE}"

# Cleanup
msg_info "Cleaning up"
rm -f headscale_${RELEASE}_linux_amd64.deb
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display setup information
msg_info "Headscale installation complete"
echo "Headscale has been installed and is running as a service."
echo "Refer to the official documentation for further configuration: https://github.com/juanfont/headscale"
