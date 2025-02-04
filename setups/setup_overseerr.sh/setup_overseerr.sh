#!/usr/bin/env  

# Name: setup_overseerr.sh
# Description: Script to install Overseerr on Debian-based systems
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
    mc \
    git \
    ca-certificates \
    gnupg
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

# Install Overseerr
msg_info "Installing Overseerr (Patience)"
git clone -q https://github.com/sct/overseerr.git /opt/overseerr
cd /opt/overseerr
yarn install
yarn build
msg_ok "Overseerr installed"

# Create Overseerr service
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/overseerr.service
[Unit]
Description=Overseerr Service
After=network.target

[Service]
Type=exec
WorkingDirectory=/opt/overseerr
ExecStart=/usr/bin/yarn start
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now overseerr.service
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Overseerr installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo -e "Overseerr is running and accessible at: \033[1;32mhttp://$IP_ADDRESS:5055\033[0m"
echo -e "Default admin setup is required on the first run."
