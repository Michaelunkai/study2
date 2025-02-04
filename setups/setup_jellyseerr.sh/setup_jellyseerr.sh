#!/usr/bin/env  

# Name: setup_jellyseerr.sh
# Description: Script to install Jellyseerr on Ubuntu 22 WSL2
# Author: Adapted for WSL2 by Assistant
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

# Update and install dependencies
msg_info "Updating system and installing dependencies"
apt-get update && apt-get upgrade -y
apt-get install -y curl sudo mc git gpg
msg_ok "System updated and dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
msg_ok "Node.js repository set up"

# Install Node.js
msg_info "Installing Node.js"
apt-get update
apt-get install -y nodejs
msg_ok "Node.js installed"

# Install pnpm
msg_info "Installing pnpm"
npm install -g pnpm
msg_ok "pnpm installed"

# Install Jellyseerr
msg_info "Installing Jellyseerr"
git clone -q https://github.com/Fallenbagel/jellyseerr.git /opt/jellyseerr
cd /opt/jellyseerr
git checkout main
export CYPRESS_INSTALL_BINARY=0
pnpm install --frozen-lockfile
export NODE_OPTIONS="--max-old-space-size=3072"
pnpm build
mkdir -p /etc/jellyseerr/
cat <<EOF >/etc/jellyseerr/jellyseerr.conf
PORT=5055
# HOST=0.0.0.0
# JELLYFIN_TYPE=emby
EOF
echo "Installed Jellyseerr version $(git describe --tags --abbrev=0)" >"/opt/jellyseerr/jellyseerr_version.txt"
msg_ok "Jellyseerr installed"

# Create and enable Jellyseerr service
msg_info "Creating and enabling Jellyseerr service"
cat <<EOF >/etc/systemd/system/jellyseerr.service
[Unit]
Description=Jellyseerr Service
After=network.target

[Service]
EnvironmentFile=/etc/jellyseerr/jellyseerr.conf
Environment=NODE_ENV=production
Type=simple
WorkingDirectory=/opt/jellyseerr
ExecStart=/usr/bin/node dist/index.js
Restart=on-failure
TimeoutStopSec=20
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

chmod +x /opt/jellyseerr/dist/index.js
chown -R root:root /opt/jellyseerr
systemctl enable --now jellyseerr.service
msg_ok "Jellyseerr service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display Web UI URL
msg_info "Jellyseerr installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Jellyseerr Web UI is accessible at: http://$IP_ADDRESS:5055"

