#!/usr/bin/env bash

# Copyright (c) 2021-2024 tteck
# Author: tteck (tteckster)
# License: MIT
# https://github.com/community-scripts/ProxmoxVE/raw/main/LICENSE

# Functions for better readability
msg_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
msg_ok() { echo -e "\033[1;32m[OK]\033[0m $1"; }
msg_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

set -e  # Exit on error

# Update and install dependencies
msg_info "Updating and installing dependencies"
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y curl sudo mc
msg_ok "Dependencies installed"

# Check if hardware acceleration is supported
msg_info "Setting up hardware acceleration"
sudo apt-get install -y va-driver-all ocl-icd-libopencl1 intel-opencl-icd vainfo intel-gpu-tools || {
  msg_error "Hardware acceleration setup failed. Skipping..."
}
if [ -d /dev/dri ]; then
  sudo chgrp video /dev/dri
  sudo chmod 755 /dev/dri
  sudo chmod 660 /dev/dri/*
  sudo usermod -aG video "$(id -u -n)"
  sudo usermod -aG render "$(id -u -n)"
  msg_ok "Hardware acceleration set up"
else
  msg_info "Hardware acceleration is not available in WSL2. Skipping..."
fi

# Install Emby
msg_info "Installing Emby Server"
LATEST=$(curl -sL https://api.github.com/repos/MediaBrowser/Emby.Releases/releases/latest | grep '"tag_name":' | cut -d'"' -f4)
wget -q "https://github.com/MediaBrowser/Emby.Releases/releases/download/${LATEST}/emby-server-deb_${LATEST}_amd64.deb"
sudo dpkg -i "emby-server-deb_${LATEST}_amd64.deb" || {
  sudo apt-get install -f -y  # Resolve dependencies if needed
  sudo dpkg -i "emby-server-deb_${LATEST}_amd64.deb"
}
msg_ok "Emby Server installed"

# Post-install cleanup
msg_info "Cleaning up"
rm -f "emby-server-deb_${LATEST}_amd64.deb"
sudo apt-get autoremove -y && sudo apt-get autoclean -y
msg_ok "Cleanup complete"

# Output WebUI URL
msg_info "Starting Emby Server"
sudo systemctl enable emby-server
sudo systemctl start emby-server
IP=$(hostname -I | awk '{print $1}')
msg_ok "Emby Server is running. Access the WebUI at: http://$IP:8096"
