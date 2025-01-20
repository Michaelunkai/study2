#!/usr/bin/env  

# Name: setup_hivemq.sh
# Description: Script to install HiveMQ CE on Ubuntu 22 WSL2
# Author: Adapted for WSL2 by Assistant
# License: MIT

# Exit on any error
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
apt-get install -y curl sudo mc gpg unzip
msg_ok "Dependencies installed"

# Install OpenJDK (Adoptium)
msg_info "Installing OpenJDK (Adoptium Temurin)"
wget -qO- https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor -o /etc/apt/trusted.gpg.d/adoptium.gpg
echo 'deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/adoptium.gpg] https://packages.adoptium.net/artifactory/deb bookworm main' > /etc/apt/sources.list.d/adoptium.list
apt-get update
apt-get install -y temurin-17-jre
msg_ok "OpenJDK installed"

# Install HiveMQ CE
msg_info "Installing HiveMQ CE"
RELEASE=$(curl -s https://api.github.com/repos/hivemq/hivemq-community-edition/releases/latest | grep "tag_name" | awk -F '"' '{print $4}')
wget -q https://github.com/hivemq/hivemq-community- ion/releases/download/${RELEASE}/hivemq-ce-${RELEASE}.zip
unzip -q hivemq-ce-${RELEASE}.zip
mkdir -p /opt/hivemq
mv hivemq-ce-${RELEASE}/* /opt/hivemq
rm -rf hivemq-ce-${RELEASE}*

# Create a dedicated user and set permissions
useradd -r -d /opt/hivemq -s /usr/sbin/nologin hivemq
chown -R hivemq:hivemq /opt/hivemq
chmod +x /opt/hivemq/bin/run.sh

# Configure HiveMQ service
cp /opt/hivemq/bin/init-script/hivemq.service /etc/systemd/system/hivemq.service
rm /opt/hivemq/conf/config.xml
mv /opt/hivemq/conf/examples/configuration/config-sample-tcp-and-websockets.xml /opt/hivemq/conf/config.xml
systemctl enable --now hivemq.service
msg_ok "HiveMQ CE installed and service started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display status
msg_info "HiveMQ installation complete"
echo "HiveMQ is running. Configuration can be found in /opt/hivemq/conf/"
