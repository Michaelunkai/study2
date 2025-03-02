#!/usr/bin/env  

# Name: setup_rdtclient.sh
# Description: Script to install RdtClient on Ubuntu
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
    mc \
    curl \
    sudo
msg_ok "Dependencies installed"

# Install ASP.NET Core Runtime
msg_info "Installing ASP.NET Core Runtime"
wget -q https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb
dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
apt-get update && apt-get install -y dotnet-sdk-9.0
msg_ok "ASP.NET Core Runtime installed"

# Install rdtclient
msg_info "Installing rdtclient"
wget -q https://github.com/rogerfar/rdt-client/releases/latest/download/RealDebridClient.zip
unzip -qq RealDebridClient.zip -d /opt/rdtc
rm RealDebridClient.zip
cd /opt/rdtc
mkdir -p data/{db,downloads}
sed -i 's#/data/db/#/opt/rdtc&#g' /opt/rdtc/appsettings.json
msg_ok "rdtclient installed"

# Create and enable rdtclient service
msg_info "Creating rdtclient service"
cat <<EOF >/etc/systemd/system/rdtc.service
[Unit]
Description=RdtClient Service
After=network.target

[Service]
WorkingDirectory=/opt/rdtc
ExecStart=/usr/bin/dotnet RdtClient.Web.dll
SyslogIdentifier=RdtClient
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now rdtc
msg_ok "rdtclient service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "RdtClient installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "RdtClient is running and accessible at: http://$IP_ADDRESS:6500"
echo "Configure your settings in the web interface."
