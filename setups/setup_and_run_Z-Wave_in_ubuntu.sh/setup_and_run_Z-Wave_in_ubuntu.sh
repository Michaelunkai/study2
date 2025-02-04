#!/usr/bin/env  

# Name: setup_zwave_js_ui.sh
# Description: Script to install Z-Wave JS UI on Ubuntu
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

# Install Z-Wave JS UI
msg_info "Installing Z-Wave JS UI"
mkdir -p /opt/zwave-js-ui
mkdir -p /opt/zwave_store
cd /opt/zwave-js-ui
RELEASE=$(curl -s https://api.github.com/repos/zwave-js/zwave-js-ui/releases/latest | grep "tag_name" | awk '{print substr($2, 2, length($2)-3) }')
wget -q https://github.com/zwave-js/zwave-js-ui/releases/download/${RELEASE}/zwave-js-ui-${RELEASE}-linux.zip
unzip -q zwave-js-ui-${RELEASE}-linux.zip
cat <<EOF >/opt/.env
ZWAVEJS_EXTERNAL_CONFIG=/opt/zwave_store/.config-db
STORE_DIR=/opt/zwave_store
EOF
echo "${RELEASE}" >"/opt/zwave-js-ui_version.txt"
msg_ok "Z-Wave JS UI installed"

# Create systemd service
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/zwave-js-ui.service
[Unit]
Description=Z-Wave JS UI
Wants=network-online.target
After=network-online.target

[Service]
User=root
WorkingDirectory=/opt/zwave-js-ui
ExecStart=/opt/zwave-js-ui/zwave-js-ui-linux
EnvironmentFile=/opt/.env

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now zwave-js-ui
msg_ok "Service created"

# Cleanup
msg_info "Cleaning up"
rm zwave-js-ui-${RELEASE}-linux.zip
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Z-Wave JS UI installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Z-Wave JS UI is running and accessible at: http://$IP_ADDRESS:8091"
echo ""
echo "### Z-Wave JS UI: Smart Home Controller"
echo "A powerful interface for managing Z-Wave networks and smart home devices."
