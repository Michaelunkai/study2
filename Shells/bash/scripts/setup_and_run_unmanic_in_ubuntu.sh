#!/usr/bin/env  

# Name: setup_unmanic.sh
# Description: Script to install Unmanic on Ubuntu
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
msg_info "Installing Dependencies (Patience)"
apt-get update && apt-get upgrade -y
apt-get install -y \
    curl \
    sudo \
    mc \
    ffmpeg \
     3-pip
msg_ok "Dependencies installed"

# Set up hardware acceleration if needed
if [[ "$CTTYPE" == "0" ]]; then
  msg_info "Setting Up Hardware Acceleration"
  apt-get install -y \
    va-driver-all \
    ocl-icd-libopencl1 \
    intel-opencl-icd
  chgrp video /dev/dri
  chmod 755 /dev/dri
  chmod 660 /dev/dri/*
  adduser $(id -u -n) video
  adduser $(id -u -n) render
  msg_ok "Hardware Acceleration set up"
fi

# Install Unmanic
msg_info "Installing Unmanic"
pip3 install unmanic
sed -i -e 's/^sgx:x:104:$/render:x:104:root/' -e 's/^render:x:106:root$/sgx:x:106:/' /etc/group
msg_ok "Unmanic installed"

# Create systemd service for Unmanic
msg_info "Creating Service"
cat << EOF >/etc/systemd/system/unmanic.service
[Unit]
Description=Unmanic - Library Optimiser
After=network-online.target
StartLimitInterval=200
StartLimitBurst=3

[Service]
Type=simple
ExecStart=/usr/local/bin/unmanic
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now unmanic.service
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Unmanic installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Unmanic is running and accessible at: http://$IP_ADDRESS:8888"
echo ""
echo "### Unmanic: Automatic Media Optimization"
echo "A tool for automating media transcoding and optimizing your library."
