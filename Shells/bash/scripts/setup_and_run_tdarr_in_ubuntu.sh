#!/usr/bin/env  

# Name: setup_tdarr.sh
# Description: Script to install Tdarr on Ubuntu
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
    handbrake-cli
msg_ok "Dependencies installed"

# Set up hardware acceleration
msg_info "Setting Up Hardware Acceleration"
apt-get install -y va-driver-all ocl-icd-libopencl1 intel-opencl-icd vainfo intel-gpu-tools
if [[ "$CTTYPE" == "0" ]]; then
  chgrp video /dev/dri
  chmod 755 /dev/dri
  chmod 660 /dev/dri/*
  adduser $(id -u -n) video
  adduser $(id -u -n) render
fi
msg_ok "Hardware Acceleration set up"

# Install Tdarr
msg_info "Installing Tdarr"
mkdir -p /opt/tdarr
cd /opt/tdarr
RELEASE=$(curl -s https://f000.backblazeb2.com/file/tdarrs/versions.json | grep -oP '(?<="Tdarr_Updater": ")[^"]+' | grep linux_x64 | head -n 1)
wget -q $RELEASE -O Tdarr_Updater.zip
unzip -q Tdarr_Updater.zip
rm -rf Tdarr_Updater.zip
chmod +x Tdarr_Updater
./Tdarr_Updater &>/dev/null

# Adjust user groups for hardware acceleration
if [[ "$CTTYPE" == "0" ]]; then
  sed -i -e 's/^sgx:x:104:$/render:x:104:root/' -e 's/^render:x:106:root$/sgx:x:106:/' /etc/group
else
  sed -i -e 's/^sgx:x:104:$/render:x:104:/' -e 's/^render:x:106:$/sgx:x:106:/' /etc/group
fi
msg_ok "Tdarr installed"

# Create systemd services
msg_info "Creating Services"

cat <<EOF >/etc/systemd/system/tdarr-server.service
[Unit]
Description=Tdarr Server Daemon
After=network.target

[Service]
User=root
Group=root
Type=simple
WorkingDirectory=/opt/tdarr/Tdarr_Server
ExecStartPre=/opt/tdarr/Tdarr_Updater
ExecStart=/opt/tdarr/Tdarr_Server/Tdarr_Server
TimeoutStopSec=20
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF >/etc/systemd/system/tdarr-node.service
[Unit]
Description=Tdarr Node Daemon
After=network.target
Requires=tdarr-server.service

[Service]
User=root
Group=root
Type=simple
WorkingDirectory=/opt/tdarr/Tdarr_Node
ExecStart=/opt/tdarr/Tdarr_Node/Tdarr_Node
TimeoutStopSec=20
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now tdarr-server.service
systemctl enable --now tdarr-node.service
msg_ok "Services created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Tdarr installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Tdarr Server is running and accessible at: http://$IP_ADDRESS:8265"
echo "Tdarr Node is running and accessible at: http://$IP_ADDRESS:8266"
echo ""
echo "### Tdarr: Media Transcoding Simplified"
echo "A distributed transcoding system for optimizing media files across multiple devices."
