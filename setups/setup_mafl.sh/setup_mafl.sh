#!/usr/bin/env  

# Name: setup_mafl.sh
# Description: Script to install Mafl on Ubuntu
# Author: Adapted for Ubuntu by Assistant
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
apt-get install -y \
  curl \
  sudo \
  mc \
  make \
  g++ \
  gcc \
  ca-certificates \
  gnupg
msg_ok "Dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
apt-get update
msg_ok "Node.js repository set up"

# Install Node.js and Yarn
msg_info "Installing Node.js and Yarn"
apt-get install -y nodejs
npm install -g npm@latest
npm install -g yarn
msg_ok "Node.js and Yarn installed"

# Download and install Mafl
RELEASE=$(curl -s https://api.github.com/repos/hywax/mafl/releases/latest | grep "tag_name" | awk -F '"' '{print $4}' | cut -c 2-)
msg_info "Installing Mafl v${RELEASE}"
wget -q https://github.com/hywax/mafl/archive/refs/tags/v${RELEASE}.tar.gz
tar -xzf v${RELEASE}.tar.gz
mkdir -p /opt/mafl/data
wget -q -O /opt/mafl/data/config.yml https://raw.githubusercontent.com/hywax/mafl/main/.example/config.yml
mv mafl-${RELEASE}/* /opt/mafl
rm -rf mafl-${RELEASE}
cd /opt/mafl
export NUXT_TELEMETRY_DISABLED=true
yarn install
yarn build
msg_ok "Installed Mafl v${RELEASE}"

# Create and enable Mafl service
msg_info "Creating and enabling Mafl service"
cat <<EOF >/etc/systemd/system/mafl.service
[Unit]
Description=Mafl
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
WorkingDirectory=/opt/mafl/
ExecStart=yarn preview

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now mafl
msg_ok "Mafl service created and started"

# Cleanup
msg_info "Cleaning up"
rm -rf v${RELEASE}.tar.gz
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message
msg_info "Mafl installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Mafl is running and accessible. Check your service or logs for details."
echo "To manage the Mafl service, use the following commands:"
echo "Start: sudo systemctl start mafl"
echo "Stop: sudo systemctl stop mafl"
echo "Restart: sudo systemctl restart mafl"
echo "Status: sudo systemctl status mafl"
