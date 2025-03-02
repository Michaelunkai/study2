#!/usr/bin/env  

# Name: setup_lazylibrarian.sh
# Description: Script to install LazyLibrarian on Ubuntu 22 WSL2
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
apt-get install -y curl sudo mc git
msg_ok "Dependencies installed"

# Install Python3 and related dependencies
msg_info "Installing Python3 and related dependencies"
apt-get install -y python3-pip python3-irc
pip install jaraco.stream python-Levenshtein soupsieve
msg_ok "Python3 dependencies installed"

# Install LazyLibrarian
msg_info "Installing LazyLibrarian"
git clone https://gitlab.com/LazyLibrarian/LazyLibrarian /opt/LazyLibrarian
msg_ok "LazyLibrarian installed"

# Create and enable LazyLibrarian service
msg_info "Creating and enabling LazyLibrarian service"
cat <<EOF >/etc/systemd/system/lazylibrarian.service
[Unit]
Description=LazyLibrarian Daemon
After=syslog.target network.target

[Service]
UMask=0002
Type=simple
ExecStart=/usr/bin/ 3 /opt/LazyLibrarian/LazyLibrarian.py
TimeoutStopSec=20
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now lazylibrarian.service
msg_ok "LazyLibrarian service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display Web UI URL
msg_info "LazyLibrarian installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "LazyLibrarian Web UI is accessible at: http://$IP_ADDRESS:5299"

# Explanation of the Tool
echo ""
echo "### Explanation of the Tool in Four Words:"
echo "**Library Management Automation Tool**"
echo ""

# Additional Commands
echo "### Additional Commands:"
echo "To organize your LazyLibrarian-related files, create and navigate into a directory named 'lazylibrarian' by running the following commands:"
echo ""
echo "  "
echo "mkdir lazylibrarian && cd lazylibrarian"
echo " "
echo ""
