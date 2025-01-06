#!/usr/bin/env  

# Name: setup_octoprint_port4444.sh
# Description: Script to install OctoPrint on Ubuntu (configured to run on port 4444)
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
    lib -dev \
    build-essential
msg_ok "Dependencies installed"

# Update Python3
msg_info "Updating Python3"
apt-get install -y \
     3 \
     3-dev \
     3-pip \
     3-venv \
     3-setuptools
rm -rf /usr/lib/ 3.*/EXTERNALLY-MANAGED
msg_ok "Python3 updated"

# Create user for OctoPrint
msg_info "Creating user octoprint"
useradd -m -s /bin/bash -p $(openssl passwd -1 octoprint) octoprint
usermod -aG sudo,tty,dialout octoprint
chown -R octoprint:octoprint /opt
echo "octoprint ALL=NOPASSWD: $(command -v systemctl) restart octoprint, $(command -v reboot), $(command -v poweroff)" > /etc/sudoers.d/octoprint
msg_ok "User octoprint created"

# Install OctoPrint
msg_info "Installing OctoPrint"
sudo -u octoprint bash <<EOF
mkdir -p /opt/octoprint
cd /opt/octoprint
python3 -m venv .
source bin/activate
pip install --upgrade pip
pip install wheel
pip install octoprint
EOF
msg_ok "OctoPrint installed"

# Configure OctoPrint to run on port 4444
msg_info "Configuring OctoPrint for port 4444"
sudo -u octoprint bash <<EOF
echo 'server:
  host: 0.0.0.0
  port: 4444
' > /opt/octoprint/config. 
EOF
msg_ok "OctoPrint configured for port 4444"

# Create systemd service for OctoPrint
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/octoprint.service
[Unit]
Description=The snappy web interface for your 3D printer
After=network-online.target
Wants=network-online.target

[Service]
Environment="LC_ALL=C.UTF-8"
Environment="LANG=C.UTF-8"
Type=exec
User=octoprint
ExecStart=/opt/octoprint/bin/octoprint serve --config /opt/octoprint/config.yaml

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now octoprint.service
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "OctoPrint installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "OctoPrint is running and accessible at: http://$IP_ADDRESS:4444"
