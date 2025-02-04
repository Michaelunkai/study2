#!/usr/bin/env  

# Name: setup_ombi.sh
# Description: Script to install Ombi on Ubuntu
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
    mc
msg_ok "Dependencies installed"

# Install Ombi
msg_info "Installing Ombi"
RELEASE=$(curl -sL https://api.github.com/repos/Ombi-app/Ombi/releases/latest | grep '"tag_name":' | cut -d'"' -f4)
wget -q https://github.com/Ombi-app/Ombi/releases/download/${RELEASE}/linux-x64.tar.gz
mkdir -p /opt/ombi
tar -xzf linux-x64.tar.gz -C /opt/ombi
rm -rf linux-x64.tar.gz
echo "${RELEASE}" >/opt/ombi_version.txt
msg_ok "Ombi installed"

# Create and enable Ombi service
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/ombi.service
[Unit]
Description=Ombi
After=syslog.target network-online.target

[Service]
ExecStart=/opt/ombi/Ombi
WorkingDirectory=/opt/ombi
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now ombi.service
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Ombi installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Ombi is running and accessible at: http://$IP_ADDRESS:5000"
