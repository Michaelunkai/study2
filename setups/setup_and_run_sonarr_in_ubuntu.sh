#!/usr/bin/env  

# Name: setup_sonarr_v4.sh
# Description: Script to install Sonarr v4 on Ubuntu
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
    curl \
    sudo \
    mc \
     ite3
msg_ok "Dependencies installed"

# Install Sonarr v4
msg_info "Installing Sonarr v4"
mkdir -p /var/lib/sonarr/
chmod 775 /var/lib/sonarr/
wget -q -O SonarrV4.tar.gz 'https://services.sonarr.tv/v1/download/main/latest?version=4&os=linux&arch=x64'
tar -xzf SonarrV4.tar.gz
mv Sonarr /opt
rm -rf SonarrV4.tar.gz
msg_ok "Sonarr v4 installed"

# Create and enable Sonarr service
msg_info "Creating Sonarr service"
cat <<EOF >/etc/systemd/system/sonarr.service
[Unit]
Description=Sonarr Daemon
After=syslog.target network.target

[Service]
Type=simple
ExecStart=/opt/Sonarr/Sonarr -nobrowser -data=/var/lib/sonarr/
TimeoutStopSec=20
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now sonarr.service
msg_ok "Sonarr service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Sonarr installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Sonarr v4 is running and accessible at: http://$IP_ADDRESS:8989"
echo "Use the web interface to configure Sonarr."
