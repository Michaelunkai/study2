#!/usr/bin/env  

# Name: setup_memos.sh
# Description: Script to install Memos on Ubuntu
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
    build-essential \
    git \
    curl \
    sudo \
    tzdata \
    mc
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

# Install pnpm
msg_info "Installing pnpm"
npm install -g pnpm
msg_ok "pnpm installed"

# Install Golang
msg_info "Installing Golang"
GOLANG=$(curl -s https://go.dev/dl/ | grep -o "go.*\linux-amd64.tar.gz" | head -n 1)
wget -q https://golang.org/dl/$GOLANG
tar -xzf $GOLANG -C /usr/local
ln -s /usr/local/go/bin/go /usr/local/bin/go
msg_ok "Golang installed"

# Install Memos
msg_info "Installing Memos (this may take a while)"
mkdir -p /opt/memos_data
git clone https://github.com/usememos/memos.git /opt/memos
cd /opt/memos/web
pnpm i --frozen-lockfile
pnpm build
cd /opt/memos
mkdir -p /opt/memos/server/dist
cp -r web/dist/* /opt/memos/server/dist/
cp -r web/dist/* /opt/memos/server/router/frontend/dist/
go build -o /opt/memos/memos -tags=embed bin/memos/main.go
msg_ok "Memos installed"

# Create and enable Memos service
msg_info "Creating Memos service"
cat <<EOF >/etc/systemd/system/memos.service
[Unit]
Description=Memos Server
After=network.target

[Service]
ExecStart=/opt/memos/memos
Environment="MEMOS_MODE=prod"
Environment="MEMOS_PORT=9030"
Environment="MEMOS_DATA=/opt/memos_data"
WorkingDirectory=/opt/memos
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now memos.service
msg_ok "Memos service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Memos installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Memos is running and accessible at: http://$IP_ADDRESS:9030"
