#!/usr/bin/env  

# Name: setup_pairdrop.sh
# Description: Script to install PairDrop on Debian-based systems
# Author: tteck
# Co-Author: havardthom
# License: MIT
# https://github.com/community-scripts/ProxmoxVE/raw/main/LICENSE

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

# Update package lists
msg_info "Updating package lists"
apt-get update
msg_ok "Package lists updated"

# Install dependencies
msg_info "Installing Dependencies"
apt-get install -y \
    curl \
    sudo \
    mc \
    git \
    gpg
msg_ok "Dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js Repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
msg_ok "Node.js repository configured"

# Install Node.js
msg_info "Installing Node.js"
apt-get update
apt-get install -y nodejs
msg_ok "Node.js installed"

# Install Yarn
msg_info "Installing Yarn"
npm install -g yarn
msg_ok "Yarn installed"

# Install PairDrop
msg_info "Installing PairDrop"
git clone -q https://github.com/schlagmichdoch/PairDrop.git /opt/pairdrop
cd /opt/pairdrop
yarn install
msg_ok "PairDrop installed"

# Create PairDrop service
msg_info "Creating PairDrop Service"
cat <<EOF >/etc/systemd/system/pairdrop.service
[Unit]
Description=PairDrop Service
After=network.target

[Service]
ExecStart=/usr/bin/yarn start
WorkingDirectory=/opt/pairdrop
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon and enable PairDrop service
systemctl daemon-reload
systemctl enable --now pairdrop.service
msg_ok "PairDrop service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with access details
msg_info "PairDrop installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo -e "PairDrop is running and accessible at: \033[1;32mhttp://$IP_ADDRESS:3000\033[0m"
echo -e "Default admin setup is required on the first run."
