#!/usr/bin/env  

# Name: setup_pingvin_share.sh
# Description: Script to install Pingvin Share on Ubuntu
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
    gnupg
msg_ok "Dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js Repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
apt-get update
msg_ok "Node.js Repository set up"

# Install Node.js and PM2
msg_info "Installing Node.js"
apt-get install -y nodejs
npm install pm2 -g
msg_ok "Node.js and PM2 installed"

# Install Pingvin Share
msg_info "Installing Pingvin Share (Patience)"
git clone -q https://github.com/stonith404/pingvin-share /opt/pingvin-share
cd /opt/pingvin-share
git fetch --tags
git checkout $(git describe --tags $(git rev-list --tags --max-count=1))

# Set up the backend
cd backend
npm install
npm run build
pm2 start --name="pingvin-share-backend" npm -- run prod

# Set up the frontend
cd ../frontend
sed -i '/"admin.config.smtp.allow-unauthorized-certificates":\|admin.config.smtp.allow-unauthorized-certificates.description":/,+1d' ./src/i18n/translations/fr-FR.ts
npm install
npm run build
pm2 start --name="pingvin-share-frontend" npm -- run start

# Enable PM2 startup and save running processes
pm2 startup systemd -u root --hp /root
pm2 save
msg_ok "Pingvin Share installed"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URLs
msg_info "Pingvin Share installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Pingvin Share is running:"
echo "  Backend: http://$IP_ADDRESS:3001"
echo "  Frontend: http://$IP_ADDRESS:3000"
