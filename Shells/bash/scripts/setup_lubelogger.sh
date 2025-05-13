#!/usr/bin/env  

# Name: setup_lubelogger.sh
# Description: Script to install LubeLogger on Ubuntu
# Author: kristocopani
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
    wget \
    mc \
    zip \
    jq
msg_ok "Dependencies installed"

# Install LubeLogger
msg_info "Installing LubeLogger"
cd /opt
mkdir -p /opt/lubelogger
RELEASE=$(curl -s https://api.github.com/repos/hargata/lubelog/releases/latest | grep "tag_name" | awk -F '"' '{print $4}' | cut -c 2-)
RELEASE_TRIMMED=$(echo "${RELEASE}" | tr -d ".")
cd /opt/lubelogger
wget -q https://github.com/hargata/lubelog/releases/download/v${RELEASE}/LubeLogger_v${RELEASE_TRIMMED}_linux_x64.zip
unzip -q LubeLogger_v${RELEASE_TRIMMED}_linux_x64.zip
chmod 700 /opt/lubelogger/CarCareTracker

# Configure application settings
cp /opt/lubelogger/appsettings.json /opt/lubelogger/appsettings_bak.json
jq '.Kestrel = {"Endpoints": {"Http": {"Url": "http://0.0.0.0:5000"}}}' /opt/lubelogger/appsettings_bak.json > /opt/lubelogger/appsettings.json
echo "${RELEASE}" >"/opt/lubelogger/lubelogger_version.txt"
msg_ok "LubeLogger installed and configured"

# Create and enable LubeLogger service
msg_info "Creating and enabling LubeLogger service"
cat <<EOF >/etc/systemd/system/lubelogger.service
[Unit]
Description=LubeLogger Daemon
After=network.target

[Service]
User=root
Type=simple
WorkingDirectory=/opt/lubelogger
ExecStart=/opt/lubelogger/CarCareTracker
TimeoutStopSec=20
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now lubelogger.service
msg_ok "LubeLogger service created and started"

# Cleanup
msg_info "Cleaning up"
rm -rf /opt/lubelogger/appsettings_bak.json
rm -rf /opt/lubelogger/LubeLogger_v${RELEASE_TRIMMED}_linux_x64.zip
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message
msg_info "LubeLogger installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "LubeLogger is running and accessible at: http://$IP_ADDRESS:5000"
echo "You can manage the service using the following commands:"
echo "Start: sudo systemctl start lubelogger"
echo "Stop: sudo systemctl stop lubelogger"
echo "Restart: sudo systemctl restart lubelogger"
echo "Status: sudo systemctl status lubelogger"
