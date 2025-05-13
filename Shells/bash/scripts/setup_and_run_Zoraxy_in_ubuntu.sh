#!/usr/bin/env  

# Name: setup_zoraxy.sh
# Description: Script to install Zoraxy on Ubuntu
# Author: tteck (tteckster)
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
    mc
msg_ok "Dependencies installed"

# Install Zoraxy
msg_info "Installing Zoraxy (Patience)"
RELEASE=$(curl -s https://api.github.com/repos/tobychui/zoraxy/releases/latest | grep "tag_name" | awk '{print substr($2, 2, length($2)-3) }')
wget -q "https://github.com/tobychui/zoraxy/releases/download/${RELEASE}/zoraxy_linux_amd64"
mkdir -p /opt/zoraxy
mv zoraxy_linux_amd64 /opt/zoraxy/zoraxy
chmod +x /opt/zoraxy/zoraxy
ln -s /opt/zoraxy/zoraxy /usr/local/bin/zoraxy
echo "${RELEASE}" >/opt/zoraxy_version.txt
msg_ok "Installed Zoraxy"

# Create systemd service
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/zoraxy.service
[Unit]
Description=General purpose request proxy and forwarding tool
After=syslog.target network-online.target

[Service]
ExecStart=/opt/zoraxy/./zoraxy
WorkingDirectory=/opt/zoraxy/
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now zoraxy.service
msg_ok "Service created"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Zoraxy installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Zoraxy is running and accessible at: http://$IP_ADDRESS:80"
echo ""
echo "### Zoraxy: Simple Proxy Forwarding Tool"
echo "Efficient and lightweight reverse proxy tool."
