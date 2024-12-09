#!/usr/bin/env bash

# Name: setup_navidrome.sh
# Description: Script to install Navidrome on Ubuntu
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
msg_info "Installing Dependencies (patience)"
apt-get update && apt-get install -y \
    curl \
    sudo \
    mc \
    ffmpeg
msg_ok "Dependencies installed"

# Get the latest Navidrome release
RELEASE=$(curl -s https://api.github.com/repos/navidrome/navidrome/releases/latest | grep "tag_name" | awk '{print substr($2, 3, length($2)-4) }')

# Install Navidrome
msg_info "Installing Navidrome"
install -d -o root -g root /opt/navidrome
install -d -o root -g root /var/lib/navidrome
wget -q https://github.com/navidrome/navidrome/releases/download/v${RELEASE}/navidrome_${RELEASE}_linux_amd64.tar.gz -O Navidrome.tar.gz
tar -xvzf Navidrome.tar.gz -C /opt/navidrome/
chown -R root:root /opt/navidrome
mkdir -p /music
cat <<EOF >/var/lib/navidrome/navidrome.toml
MusicFolder = '/music'
EOF
msg_ok "Navidrome installed"

# Create and enable Navidrome service
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/navidrome.service
[Unit]
Description=Navidrome Music Server and Streamer compatible with Subsonic/Airsonic
After=remote-fs.target network.target
AssertPathExists=/var/lib/navidrome

[Service]
User=root
Group=root
Type=simple
ExecStart=/opt/navidrome/navidrome --configfile '/var/lib/navidrome/navidrome.toml'
WorkingDirectory=/var/lib/navidrome
TimeoutStopSec=20
KillMode=process
Restart=on-failure
DevicePolicy=closed
NoNewPrivileges=yes
PrivateTmp=yes
PrivateUsers=yes
ProtectControlGroups=yes
ProtectKernelModules=yes
ProtectKernelTunables=yes
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
RestrictNamespaces=yes
RestrictRealtime=yes
SystemCallFilter=~@clock @debug @module @mount @obsolete @reboot @setuid @swap
ReadWritePaths=/var/lib/navidrome
ProtectSystem=full

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now navidrome.service
msg_ok "Service created"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
rm -rf /root/Navidrome.tar.gz
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Navidrome installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Navidrome is running and accessible at: http://$IP_ADDRESS:4533"
echo "To configure and upload your music, ensure that '/music' is accessible and populated."
