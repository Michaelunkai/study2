#!/usr/bin/env  

# Name: setup_ipfs.sh
# Description: Script to install IPFS on Ubuntu 22 WSL2
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
apt-get install -y curl sudo mc gpg
msg_ok "Dependencies installed"

# Install IPFS
msg_info "Installing IPFS"
RELEASE=$(wget -q https://github.com/ipfs/kubo/releases/latest -O - | grep "title>Release" | cut -d " " -f 4)
wget -q "https://github.com/ipfs/kubo/releases/download/${RELEASE}/kubo_${RELEASE}_linux-amd64.tar.gz"
tar -xzf "kubo_${RELEASE}_linux-amd64.tar.gz" -C /usr/local
ln -s /usr/local/kubo/ipfs /usr/local/bin/ipfs
ipfs init
ipfs config Addresses.API /ip4/0.0.0.0/tcp/5001
ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080
LXCIP=$(hostname -I | awk '{print $1}')
ipfs config --json API.HTTPHeaders.Access-Control-Allow-Origin "[\"http://${LXCIP}:5001\", \"http://localhost:3000\", \"http://127.0.0.1:5001\", \"https://webui.ipfs.io\", \"http://0.0.0.0:5001\"]"
ipfs config --json API.HTTPHeaders.Access-Control-Allow-Methods '["PUT", "POST"]'
echo "${RELEASE}" >"/opt/ipfs_version.txt"
rm "kubo_${RELEASE}_linux-amd64.tar.gz"
msg_ok "IPFS installed and configured"

# Create and enable IPFS service
msg_info "Creating and enabling IPFS service"
cat <<EOF >/etc/systemd/system/ipfs.service
[Unit]
Description=IPFS Daemon
After=syslog.target network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/ipfs daemon
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
systemctl enable --now ipfs.service
msg_ok "IPFS service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display Web UI URL and setup summary
msg_info "IPFS installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "IPFS is running and accessible through the following endpoints:"
echo "- API: http://$IP_ADDRESS:5001"
echo "- Gateway: http://$IP_ADDRESS:8080"
echo "- Web UI: https://webui.ipfs.io"

# Explanation of the Tool
echo ""
echo "### Explanation of the Tool in Four Words:"
echo "**Distributed File Storage System**"
echo ""

# Additional Commands
echo "### Additional Commands:"
echo "To organize your IPFS-related files, create and navigate into a directory named 'ipfs' by running the following commands:"
echo ""
echo "  "
echo "mkdir ipfs && cd ipfs"
echo " "
echo ""
