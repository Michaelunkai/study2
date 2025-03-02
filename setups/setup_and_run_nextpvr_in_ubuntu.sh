#!/usr/bin/env  

# Name: setup_nextpvr.sh
# Description: Script to install NextPVR on Ubuntu
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
msg_info "Installing dependencies (Patience)"
apt-get update && apt-get install -y \
    mediainfo \
    libmediainfo-dev \
    libc6 \
    curl \
    sudo \
    libgdiplus \
    acl \
    dvb-tools \
    libdvbv5-0 \
    dtv-scan-tables \
    libc6-dev \
    ffmpeg \
    mc
msg_ok "Dependencies installed"

# Setup NextPVR
msg_info "Setting up NextPVR (Patience)"
cd /opt
wget -q https://nextpvr.com/nextpvr-helper.deb
dpkg -i nextpvr-helper.deb
msg_ok "NextPVR installed"

# Cleanup
msg_info "Cleaning up"
rm -rf /opt/nextpvr-helper.deb
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "NextPVR installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "NextPVR is running and accessible at: http://$IP_ADDRESS:8866"
echo "Visit the NextPVR web interface to configure tuners and recordings."
