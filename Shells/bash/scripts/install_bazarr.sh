#!/usr/bin/env bash

# Bazarr Installer for Ubuntu 22.04 on WSL2
# Author: Adapted by AI
# License: MIT

set -euo pipefail

# Define utility functions
msg_info() {
    echo -e "\e[1;34m[INFO]\e[0m $1"
}
msg_ok() {
    echo -e "\e[1;32m[OK]\e[0m $1"
}
msg_error() {
    echo -e "\e[1;31m[ERROR]\e[0m $1"
}

# Update and upgrade the system
msg_info "Updating the system"
sudo apt-get update && sudo apt-get upgrade -y
msg_ok "System updated"

# Install dependencies
msg_info "Installing Dependencies"
sudo apt-get install -y curl sudo mc unzip wget python3 python3-dev python3-pip
msg_ok "Installed Dependencies"

# Install Bazarr
msg_info "Installing Bazarr"
BAZARR_DIR="/opt/bazarr"
BAZARR_DATA="/var/lib/bazarr"

sudo mkdir -p $BAZARR_DATA
wget -q https://github.com/morpheus65535/bazarr/releases/latest/download/bazarr.zip -O /tmp/bazarr.zip
sudo unzip -qq /tmp/bazarr.zip -d $BAZARR_DIR
sudo chmod -R 775 $BAZARR_DIR $BAZARR_DATA
python3 -m pip install -q -r $BAZARR_DIR/requirements.txt
msg_ok "Installed Bazarr"

# Create systemd service for Bazarr
msg_info "Creating Bazarr service"
sudo bash -c "cat > /etc/systemd/system/bazarr.service" <<EOF
[Unit]
Description=Bazarr Daemon
After=syslog.target network.target

[Service]
WorkingDirectory=$BAZARR_DIR
UMask=0002
Restart=on-failure
RestartSec=5
Type=simple
ExecStart=/usr/bin/python3 $BAZARR_DIR/bazarr.py
KillSignal=SIGINT
TimeoutStopSec=20
SyslogIdentifier=bazarr

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now bazarr
msg_ok "Created and started Bazarr service"

# Cleanup
msg_info "Cleaning up"
rm -rf /tmp/bazarr.zip
sudo apt-get autoremove -y
sudo apt-get autoclean -y
msg_ok "Cleanup completed"

# Echo Web UI URL
BAZARR_PORT=6767
msg_ok "Bazarr is running. Access the web UI at: http://$(hostname -I | awk '{print $1}'):$BAZARR_PORT"
