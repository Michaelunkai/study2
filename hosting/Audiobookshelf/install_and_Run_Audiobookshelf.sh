#!/usr/bin/env bash

# Copyright (c) 2021-2024 tteck
# Author: tteck (tteckster)
# License: MIT
# https://github.com/community-scripts/ProxmoxVE/raw/main/LICENSE

set -e

# Define helper functions
msg_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

msg_ok() {
    echo -e "\033[1;32m[OK]\033[0m $1"
}

msg_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
    exit 1
}

# Update and upgrade the OS
msg_info "Updating and upgrading OS"
sudo apt-get update && sudo apt-get -y upgrade
msg_ok "System updated"

# Install dependencies
msg_info "Installing dependencies"
sudo apt-get install -y curl sudo gnupg mc
msg_ok "Installed dependencies"

# Install audiobookshelf
msg_info "Installing audiobookshelf"
curl -fsSL https://advplyr.github.io/audiobookshelf-ppa/KEY.gpg | sudo tee /etc/apt/trusted.gpg.d/audiobookshelf-ppa.asc > /dev/null
echo "deb [signed-by=/etc/apt/trusted.gpg.d/audiobookshelf-ppa.asc] https://advplyr.github.io/audiobookshelf-ppa ./" | sudo tee /etc/apt/sources.list.d/audiobookshelf.list > /dev/null
sudo apt-get update
sudo apt-get install -y audiobookshelf
msg_ok "Installed audiobookshelf"

# Clean up
msg_info "Cleaning up"
sudo apt-get -y autoremove
sudo apt-get -y autoclean
msg_ok "System cleaned"

# Start audiobookshelf and display WebUI URL
msg_info "Starting audiobookshelf service"
sudo systemctl enable --now audiobookshelf
msg_ok "Audiobookshelf started"

# Output the URL for the WebUI
WEBUI_URL="http://$(hostname -I | awk '{print $1}'):13378"
echo -e "\033[1;36m[INFO]\033[0m Audiobookshelf WebUI available at: $WEBUI_URL"
