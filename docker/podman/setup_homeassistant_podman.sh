#!/usr/bin/env bash

# Name: setup_homeassistant_podman.sh
# Description: Script to install Home Assistant on Ubuntu using Podman
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
    mc
msg_ok "Dependencies installed"

# Install Podman
msg_info "Installing Podman"
apt-get -y install podman
systemctl enable --now podman.socket
msg_ok "Podman installed and socket enabled"

# Pull Home Assistant image
msg_info "Pulling Home Assistant Image"
podman pull docker.io/homeassistant/home-assistant:stable
msg_ok "Home Assistant image pulled"

# Install Home Assistant
msg_info "Installing Home Assistant"
podman volume create hass_config
podman run -d \
  --name homeassistant \
  --restart unless-stopped \
  -v /dev:/dev \
  -v hass_config:/config \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  --net=host \
  homeassistant/home-assistant:stable
podman generate systemd \
  --new --name homeassistant \
  >/etc/systemd/system/homeassistant.service
systemctl enable --now homeassistant
msg_ok "Home Assistant installed and running"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with access URL
msg_info "Home Assistant installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Home Assistant is running and accessible at: http://$IP_ADDRESS:8123"
