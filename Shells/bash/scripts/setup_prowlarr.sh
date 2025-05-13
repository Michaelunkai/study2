#!/usr/bin/env  

# Name: setup_prowlarr.sh
# Description: Script to install Prowlarr on Ubuntu
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
     ite3
msg_ok "Dependencies installed"

# Install Prowlarr
msg_info "Installing Prowlarr"
mkdir -p /var/lib/prowlarr/
chmod 775 /var/lib/prowlarr/
wget --content-disposition 'https://prowlarr.servarr.com/v1/update/master/updatefile?os=linux&runtime=netcore&arch=x64'
tar -xvzf Prowlarr.master.*.tar.gz
mv Prowlarr /opt
chmod 775 /opt/Prowlarr
rm -rf Prowlarr.master.*.tar.gz
msg_ok "Prowlarr installed"

# Create and enable Prowlarr service
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/prowlarr.service
[Unit]
Description=Prowlarr Daemon
After=syslog.target network.target

[Service]
UMask=0002
Type=simple
ExecStart=/opt/Prowlarr/Prowlarr -nobrowser -data=/var/lib/prowlarr/
TimeoutStopSec=20
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl -q daemon-reload
systemctl enable --now -q prowlarr
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Prowlarr installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Prowlarr is running and accessible at: http://$IP_ADDRESS:9696"
