#!/usr/bin/env  

# Name: setup_omada_controller.sh
# Description: Script to install TP-Link Omada Controller on Ubuntu
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
    gnupg \
    jsvc
msg_ok "Dependencies installed"

# Install Azul Zulu (Java)
msg_info "Installing Azul Zulu"
wget -qO /etc/apt/trusted.gpg.d/zulu-repo.asc "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xB1998361219BD9C9"
wget -q https://cdn.azul.com/zulu/bin/zulu-repo_1.0.0-3_all.deb
dpkg -i zulu-repo_1.0.0-3_all.deb
apt-get update
apt-get -y install zulu8-jdk
msg_ok "Azul Zulu installed"

# Install MongoDB
msg_info "Installing MongoDB"
libssl=$(curl -fsSL "http://security.ubuntu.com/ubuntu/pool/main/o/openssl/" | grep -o 'libssl1\.1_1\.1\.1f-1ubuntu2\.2[^"]*amd64\.deb' | head -n1)
wget -q http://security.ubuntu.com/ubuntu/pool/main/o/openssl/$libssl
dpkg -i $libssl
wget -q https://repo.mongodb.org/apt/ubuntu/dists/bionic/mongodb-org/3.6/multiverse/binary-amd64/mongodb-org-server_3.6.23_amd64.deb
dpkg -i mongodb-org-server_3.6.23_amd64.deb
msg_ok "MongoDB installed"

# Fetch the latest Omada Controller version
latest_url=$(curl -fsSL "https://www.tp-link.com/en/support/download/omada-software-controller/" | grep -o 'https://.*x64.deb' | head -n1)
latest_version=$(basename "$latest_url")

# Install Omada Controller
msg_info "Installing Omada Controller"
wget -q ${latest_url}
dpkg -i ${latest_version}
msg_ok "Omada Controller installed"

# Cleanup
msg_info "Cleaning up"
rm -rf ${latest_version} mongodb-org-server_3.6.23_amd64.deb zulu-repo_1.0.0-3_all.deb $libssl
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Omada Controller installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Omada Controller is running and accessible at: https://$IP_ADDRESS:8043"
echo "Log in to the Omada Controller interface to configure your network."
