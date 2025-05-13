#!/usr/bin/env bash

# Updated for Ubuntu 22.04 on WSL2
# Tool: Cronicle (Task Scheduler & Monitor)
# Author: tteck (tteckster), Modified by ChatGPT
# License: MIT

set -e

# Function to display messages
function msg_info() {
    echo -e "\e[34m[INFO]\e[0m $1"
}

function msg_ok() {
    echo -e "\e[32m[OK]\e[0m $1"
}

function msg_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
}

# Update and install dependencies
msg_info "Updating system and installing dependencies"
sudo apt-get update
sudo apt-get install -y curl sudo mc git make g++ gcc
msg_ok "Dependencies installed"

# Install Node.js using NVM
msg_info "Installing Node.js"
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"
nvm install 16.20.1
sudo ln -sf "$HOME/.nvm/versions/node/v16.20.1/bin/node" /usr/bin/node
msg_ok "Node.js installed"

# Install Cronicle
msg_info "Installing Cronicle Primary Server"
LATEST=$(curl -sL https://api.github.com/repos/jhuckaby/Cronicle/releases/latest | grep '"tag_name":' | cut -d'"' -f4)
IP=$(hostname -I | awk '{print $1}')
sudo mkdir -p /opt/cronicle
cd /opt/cronicle
curl -fsSL https://github.com/jhuckaby/Cronicle/archive/${LATEST}.tar.gz | sudo tar zxvf - --strip-components 1
sudo npm install
sudo node bin/build.js dist
sudo sed -i "s/localhost:3012/${IP}:3012/g" /opt/cronicle/conf/config.json
sudo /opt/cronicle/bin/control.sh setup
sudo /opt/cronicle/bin/control.sh start
msg_ok "Cronicle installed and started"

# Output web UI URL
WEB_UI="http://${IP}:3012"
echo -e "\n\e[32mCronicle Web UI available at: ${WEB_UI}\e[0m"

# Cleanup
msg_info "Cleaning up"
sudo apt-get -y autoremove
sudo apt-get -y autoclean
msg_ok "Cleanup complete"
