#!/usr/bin/env  

# Name: setup_iobroker.sh
# Description: Script to install and configure ioBroker on Ubuntu 22 WSL2
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
apt-get install -y curl sudo mc apt-transport-https composer php php-cli php-fpm php-json php-common php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath
msg_ok "Dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
msg_ok "Set up Node.js Repository"

# Install Node.js
msg_info "Installing Node.js"
apt-get update
apt-get install -y nodejs
msg_ok "Installed Node.js"

# Install ioBroker
msg_info "Installing ioBroker (Patience)"
bash <(curl -fsSL https://iobroker.net/install.sh) --install
msg_ok "Installed ioBroker"

# Create a dedicated user for ioBroker (optional but recommended)
msg_info "Creating ioBroker user"
useradd -r -d /opt/iobroker -s /usr/sbin/nologin iobroker || true
chown -R iobroker:iobroker /opt/iobroker
msg_ok "ioBroker user created"

# Create Systemd Service for ioBroker
msg_info "Creating ioBroker service"
cat <<EOF >/etc/systemd/system/iobroker.service
[Unit]
Description=ioBroker Service
After=network.target

[Service]
Type=simple
User=iobroker
Group=iobroker
WorkingDirectory=/opt/iobroker
ExecStart=/usr/bin/node /opt/iobroker/iobroker.js start
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
msg_ok "ioBroker service file created"

# Reload systemd daemon to recognize the new service
msg_info "Reloading systemd daemon"
systemctl daemon-reload
msg_ok "Systemd daemon reloaded"

# Enable and Start ioBroker Service
msg_info "Enabling and starting ioBroker service"
systemctl enable --now iobroker.service
msg_ok "ioBroker service enabled and started"

# Verify the service status
msg_info "Verifying ioBroker service status"
if systemctl is-active --quiet iobroker.service; then
    msg_ok "ioBroker service is running"
else
    msg_error "ioBroker service failed to start. Please check the service logs using 'journalctl -u iobroker.service'"
fi

# Echo the Web UI URL
IOBROKER_PORT=8081  # Default port for ioBroker Web UI; change if configured differently
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "ioBroker Web UI is accessible at: http://${IP_ADDRESS}:${IOBROKER_PORT}"
msg_ok "ioBroker installation complete"

# Customize MOTD and SSH (Assuming functions are defined elsewhere)
# Uncomment the following lines if motd_ssh and customize functions are available
# motd_ssh
# customize

# Cleanup
msg_info "Cleaning up"
apt-get -y autoremove
apt-get -y autoclean
msg_ok "Cleanup complete"
