#!/usr/bin/env  

# Name: setup_spoolman.sh
# Description: Script to install Spoolman on Ubuntu
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
msg_info "Installing dependencies"
apt-get update && apt-get install -y \
    build-essential \
    curl \
    sudo \
    make \
    libpq-dev \
    gpg \
    ca-certificates \
    mc
msg_ok "Dependencies installed"

# Install Python3
msg_info "Installing Python3"
apt-get install -y \
     3-dev \
     3-setuptools \
     3-wheel \
     3-pip
msg_ok "Python3 installed"

# Install Spoolman
msg_info "Installing Spoolman"
RELEASE=$(wget -q https://github.com/Donkie/Spoolman/releases/latest -O - | grep "title>Release" | cut -d " " -f 4)
cd /opt
wget -q https://github.com/Donkie/Spoolman/releases/download/$RELEASE/spoolman.zip
unzip -q spoolman.zip -d spoolman
rm -rf spoolman.zip
cd spoolman
pip3 install -r requirements.txt
wget -q https://raw.githubusercontent.com/Donkie/Spoolman/master/.env.example -O .env
echo "${RELEASE}" >/opt/spoolman_version.txt
msg_ok "Spoolman installed"

# Create and enable Spoolman service
msg_info "Creating Spoolman service"
cat <<EOF >/etc/systemd/system/spoolman.service
[Unit]
Description=Spoolman
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/spoolman
EnvironmentFile=/opt/spoolman/.env
ExecStart=/usr/local/bin/uvicorn spoolman.main:app --host 0.0.0.0 --port 7912
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now spoolman.service
msg_ok "Spoolman service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Spoolman installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Spoolman is running and accessible at: http://$IP_ADDRESS:7912"
