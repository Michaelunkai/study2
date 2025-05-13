#!/usr/bin/env  

# Name: setup_triliumnext.sh
# Description: Script to install TriliumNext on Ubuntu
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
    mc
msg_ok "Dependencies installed"

# Fetch the latest release of TriliumNext
RELEASE=$(curl -s https://api.github.com/repos/TriliumNext/Notes/releases/latest | grep "tag_name" | awk '{print substr($2, 2, length($2)-3) }')

# Install TriliumNext
msg_info "Installing TriliumNext"
wget -q https://github.com/TriliumNext/Notes/releases/download/${RELEASE}/TriliumNextNotes-${RELEASE}-server-linux-x64.tar.xz
tar -xf TriliumNextNotes-${RELEASE}-server-linux-x64.tar.xz
mv trilium-linux-x64-server /opt/trilium
msg_ok "TriliumNext installed"

# Create a systemd service for TriliumNext
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/trilium.service
[Unit]
Description=TriliumNext Daemon
After=syslog.target network.target

[Service]
User=root
Type=simple
ExecStart=/opt/trilium/trilium.sh
WorkingDirectory=/opt/trilium/
TimeoutStopSec=20
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now trilium
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
rm -rf TriliumNextNotes-${RELEASE}-server-linux-x64.tar.xz
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "TriliumNext installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "TriliumNext is running and accessible at: http://$IP_ADDRESS:8080"
echo ""
echo "### TriliumNext: Personal Note-Taking Application"
echo "A modern, self-hosted, hierarchical note-taking application."
