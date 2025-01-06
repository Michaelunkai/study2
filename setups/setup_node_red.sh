#!/usr/bin/env  

# Name: setup_node_red.sh
# Description: Script to install Node-RED on Ubuntu
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
apt-get update && apt-get upgrade -y
apt-get install -y \
    curl \
    sudo \
    mc \
    git \
    ca-certificates \
    gnupg
msg_ok "Dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
apt-get update
msg_ok "Node.js repository set up"

# Install Node.js
msg_info "Installing Node.js"
apt-get install -y nodejs
msg_ok "Node.js installed"

# Install Node-RED
msg_info "Installing Node-RED"
npm install -g --unsafe-perm node-red
echo "journalctl -f -n 100 -u nodered -o cat" >/usr/bin/node-red-log
chmod +x /usr/bin/node-red-log
echo "systemctl stop nodered" >/usr/bin/node-red-stop
chmod +x /usr/bin/node-red-stop
echo "systemctl start nodered" >/usr/bin/node-red-start
chmod +x /usr/bin/node-red-start
echo "systemctl restart nodered" >/usr/bin/node-red-restart
chmod +x /usr/bin/node-red-restart
msg_ok "Node-RED installed"

# Create and enable Node-RED service
msg_info "Creating Node-RED service"
cat <<EOF >/etc/systemd/system/nodered.service
[Unit]
Description=Node-RED
After=syslog.target network.target

[Service]
ExecStart=/usr/bin/node-red --max-old-space-size=128 -v
Restart=on-failure
KillSignal=SIGINT

SyslogIdentifier=node-red
Standard =syslog

WorkingDirectory=/root/
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now nodered.service
msg_ok "Node-RED service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Node-RED installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Node-RED is running and accessible at: http://$IP_ADDRESS:1880"
echo "Use the command 'node-red-log' to view the logs."
