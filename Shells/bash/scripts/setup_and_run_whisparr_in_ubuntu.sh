#!/usr/bin/env  

# Name: setup_whisparr.sh
# Description: Script to install Whisparr on Ubuntu
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
apt-get update && apt-get upgrade -y
apt-get install -y \
    curl \
    sudo \
    mc \
     ite3
msg_ok "Dependencies installed"

# Install Whisparr
msg_info "Installing Whisparr"
mkdir -p /var/lib/whisparr/
chmod 775 /var/lib/whisparr/
wget --content-disposition 'https://whisparr.servarr.com/v1/update/nightly/updatefile?os=linux&runtime=netcore&arch=x64'
tar -xvzf Whisparr.develop.*.tar.gz
mv Whisparr /opt
chmod 775 /opt/Whisparr
msg_ok "Whisparr installed"

# Create a systemd service for Whisparr
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/whisparr.service
[Unit]
Description=Whisparr Daemon
After=syslog.target network.target

[Service]
UMask=0002
Type=simple
ExecStart=/opt/Whisparr/Whisparr -nobrowser -data=/var/lib/whisparr/
TimeoutStopSec=20
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now whisparr
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
rm -rf Whisparr.develop.*.tar.gz
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Whisparr installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Whisparr is running and accessible at: http://$IP_ADDRESS:6969"
echo ""
echo "### Whisparr: Anime Collection Management Tool"
echo "A fork of Radarr specifically designed for anime library management and organization."
