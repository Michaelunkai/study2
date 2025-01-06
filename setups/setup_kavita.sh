#!/usr/bin/env  

# Name: setup_kavita.sh
# Description: Script to install Kavita on Ubuntu 22 WSL2
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
apt-get install -y curl sudo mc
msg_ok "System updated and dependencies installed"

# Install Kavita
msg_info "Installing Kavita"
KAVITA_REPO="Kareadita/Kavita"
RELEASE=$(curl -s https://api.github.com/repos/${KAVITA_REPO}/releases/latest | grep "tag_name" | awk -F '"' '{print $4}')
wget -qO- https://github.com/${KAVITA_REPO}/releases/download/${RELEASE}/kavita-linux-x64.tar.gz | tar -xzf - -C /opt
chmod +x /opt/Kavita/Kavita
msg_ok "Kavita installed"

# Configure environment variables
msg_info "Configuring Kavita"
cat <<EOF >/opt/Kavita/.env
# Configuration for Kavita
KAVITA_MODE=production
KAVITA_WEB_PORT=5000
KAVITA_WEB_HOST=0.0.0.0
EOF
echo "${RELEASE}" >"/opt/Kavita/kavita_version.txt"
msg_ok "Kavita configured"

# Create and enable Kavita service
msg_info "Creating and enabling Kavita service"
cat <<EOF >/etc/systemd/system/kavita.service
[Unit]
Description=Kavita Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/Kavita
ExecStart=/opt/Kavita/Kavita
EnvironmentFile=/opt/Kavita/.env
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

chmod +x /opt/Kavita/Kavita
chown -R root:root /opt/Kavita
systemctl enable --now kavita.service
msg_ok "Kavita service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display Web UI URL
msg_info "Kavita installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Kavita Web UI is accessible at: http://$IP_ADDRESS:5000"

# Run the tool (ensure it's running)
msg_info "Starting Kavita service"
systemctl start kavita.service
msg_ok "Kavita service started"

