#!/usr/bin/env  

# Name: setup_whoogle.sh
# Description: Script to install Whoogle Search on Ubuntu
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

# Update Python3
msg_info "Updating Python3"
apt-get install -y \
     3 \
     3-dev \
     3-pip
rm -rf /usr/lib/ 3.*/EXTERNALLY-MANAGED
msg_ok "Python3 updated"

# Install Whoogle
msg_info "Installing Whoogle"
pip install brotli
pip install whoogle-search

# Create systemd service for Whoogle
cat <<EOF >/etc/systemd/system/whoogle.service
[Unit]
Description=Whoogle Search
After=network.target

[Service]
ExecStart=/usr/local/bin/whoogle-search --host 0.0.0.0
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now whoogle.service
msg_ok "Whoogle installed and service started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Whoogle installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Whoogle Search is running and accessible at: http://$IP_ADDRESS:5000"
echo ""
echo "### Whoogle: Private Google Search Alternative"
echo "A self-hosted, ad-free, and privacy-friendly search engine."
