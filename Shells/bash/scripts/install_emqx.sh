#!/usr/bin/env bash

# EMQX Installer Script for Ubuntu 22 WSL2
# Copyright (c) 2021-2024 tteck
# Author: tteck (tteckster)
# License: MIT
# https://github.com/community-scripts/ProxmoxVE/raw/main/LICENSE

set -euo pipefail

# Helper functions
function msg_info {
    echo -e "\e[34m[INFO]\e[0m $1"
}

function msg_ok {
    echo -e "\e[32m[OK]\e[0m $1"
}

function catch_errors {
    echo -e "\e[31m[ERROR]\e[0m An error occurred. Exiting."
    exit 1
}

trap catch_errors ERR

msg_info "Updating System and Installing Dependencies"
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y curl sudo mc
msg_ok "System and Dependencies Updated"

msg_info "Installing EMQX"
curl -fsSL https://packagecloud.io/install/repositories/emqx/emqx/script.deb.sh | sudo bash
sudo apt-get install -y emqx
sudo systemctl enable --now emqx
msg_ok "Installed and Started EMQX"

msg_info "Cleaning Up"
sudo apt-get autoremove -y
sudo apt-get autoclean -y
msg_ok "Cleaned Up"

msg_info "Fetching WebUI URL"
IP=$(hostname -I | awk '{print $1}')
WEBUI_URL="http://${IP}:18083"
msg_ok "WebUI available at: ${WEBUI_URL}"

echo -e "\nAccess EMQX WebUI: ${WEBUI_URL}\n"
