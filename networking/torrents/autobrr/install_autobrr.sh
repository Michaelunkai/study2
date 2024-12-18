#!/usr/bin/env bash

# Autobrr Installation Script for Ubuntu 22.04 (WSL2)
# Copyright (c) 2021-2024 tteck
# Author: tteck (tteckster)
# License: MIT
# https://github.com/community-scripts/ProxmoxVE/raw/main/LICENSE

set -e

# Define helper functions
function msg_info() {
    echo -e "\e[32m[INFO] $1\e[0m"
}

function msg_ok() {
    echo -e "\e[32m[OK] $1\e[0m"
}

function msg_error() {
    echo -e "\e[31m[ERROR] $1\e[0m"
    exit 1
}

# Update and install dependencies
msg_info "Updating system and installing dependencies"
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y curl sudo mc openssl
msg_ok "System updated and dependencies installed"

# Install Autobrr
msg_info "Installing Autobrr"
DOWNLOAD_URL=$(curl -s https://api.github.com/repos/autobrr/autobrr/releases/latest | grep linux_x86_64 | grep -oP '(?<=browser_download_url": ")[^"]+')
wget -q "$DOWNLOAD_URL" -O autobrr.tar.gz
sudo tar -C /usr/local/bin -xzf autobrr.tar.gz
rm -f autobrr.tar.gz
msg_ok "Autobrr downloaded and extracted"

# Configure Autobrr
msg_info "Configuring Autobrr"
CONFIG_DIR="/root/.config/autobrr"
mkdir -p "$CONFIG_DIR"
cat <<EOF >"$CONFIG_DIR/config.toml"
host = "0.0.0.0"
port = 7474
logLevel = "DEBUG"
sessionSecret = "$(openssl rand -base64 24)"
EOF
msg_ok "Autobrr configured"

# Create and enable service
msg_info "Creating and enabling Autobrr service"
SERVICE_FILE="/etc/systemd/system/autobrr.service"
sudo bash -c "cat <<EOL >$SERVICE_FILE
[Unit]
Description=Autobrr service
After=syslog.target network-online.target

[Service]
Type=simple
User=root
Group=root
ExecStart=/usr/local/bin/autobrr --config=/root/.config/autobrr/

[Install]
WantedBy=multi-user.target
EOL"
sudo systemctl daemon-reload
sudo systemctl enable --now autobrr.service
msg_ok "Autobrr service created and started"

# Clean up
msg_info "Cleaning up"
sudo apt-get autoremove -y && sudo apt-get autoclean -y
msg_ok "Clean-up completed"

# Output WebUI URL
WEBUI_URL="http://localhost:7474"
msg_ok "Autobrr is installed and running. Access the web interface at: $WEBUI_URL"
echo $WEBUI_URL
