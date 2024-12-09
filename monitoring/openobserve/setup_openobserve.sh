#!/usr/bin/env  

# Name: setup_openobserve.sh
# Description: Script to install OpenObserve on Debian-based systems
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
    mc
msg_ok "Dependencies installed"

# Install OpenObserve
msg_info "Installing OpenObserve"
mkdir -p /opt/openobserve/data
LATEST=$(curl -sL https://api.github.com/repos/openobserve/openobserve/releases/latest | grep '"tag_name":' | cut -d'"' -f4)
tar zxvf <(curl -fsSL https://github.com/openobserve/openobserve/releases/download/$LATEST/openobserve-${LATEST}-linux-amd64.tar.gz) -C /opt/openobserve

ROOT_EMAIL="admin@example.com"
ROOT_PASSWORD=$(openssl rand -base64 18 | cut -c1-13)

cat <<EOF >/opt/openobserve/data/.env
ZO_ROOT_USER_EMAIL=$ROOT_EMAIL
ZO_ROOT_USER_PASSWORD=$ROOT_PASSWORD
ZO_DATA_DIR=/opt/openobserve/data
ZO_HTTP_PORT=5080
EOF
msg_ok "OpenObserve installed"

# Create OpenObserve service
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/openobserve.service
[Unit]
Description=OpenObserve
After=network.target

[Service]
Type=simple
EnvironmentFile=/opt/openobserve/data/.env
ExecStart=/opt/openobserve/openobserve
ExecStop=killall -QUIT openobserve
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now openobserve.service
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and credentials
msg_info "OpenObserve installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo -e "OpenObserve is running and accessible at: \033[1;32mhttp://$IP_ADDRESS:5080\033[0m"
echo -e "Login with the following credentials:"
echo -e "  Email: \033[1;32m$ROOT_EMAIL\033[0m"
echo -e "  Password: \033[1;32m$ROOT_PASSWORD\033[0m"

