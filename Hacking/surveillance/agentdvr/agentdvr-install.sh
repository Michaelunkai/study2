#!/usr/bin/env bash

# =============================================================================
# Title:        Install AgentDVR on Ubuntu 22.04 WSL2
# Description:  This script installs AgentDVR along with necessary dependencies
#               on Ubuntu 22.04 running under WSL2.
# Author:       Your Name
# License:      MIT
# =============================================================================

set -e

# ------------------------------- Functions -----------------------------------

# Function to display informational messages
msg_info() {
    echo -e "\e[34m[INFO]\e[0m $1"
}

# Function to display success messages
msg_ok() {
    echo -e "\e[32m[OK]\e[0m $1"
}

# Function to display error messages and exit
msg_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
    exit 1
}

# Function to check if running inside WSL
is_wsl() {
    grep -qi microsoft /proc/version || grep -qi wsl /proc/version 2>/dev/null
}

# Function to install dependencies
install_dependencies() {
    msg_info "Installing Dependencies"
    sudo apt-get update -y
    sudo apt-get install -y \
        curl \
        sudo \
        mc \
        unzip \
        apt-transport-https \
        alsa-utils \
        libxext-dev \
        fontconfig \
        libva-drm2 \
        wget
    msg_ok "Installed Dependencies"
}

# Function to install AgentDVR
install_agentdvr() {
    msg_info "Installing AgentDVR"
    sudo mkdir -p /opt/agentdvr/agent
    RELEASE_URL=$(curl -s "https://www.ispyconnect.com/api/Agent/DownloadLocation4?platform=Linux64&fromVersion=0" | grep -o 'https://[^"]*\.zip')
    
    if [[ -z "$RELEASE_URL" ]]; then
        msg_error "Failed to fetch AgentDVR release URL."
    fi

    cd /opt/agentdvr/agent || msg_error "Failed to navigate to /opt/agentdvr/agent"

    sudo wget -q "$RELEASE_URL" -O AgentDVR.zip
    sudo unzip -o AgentDVR.zip
    sudo rm -f AgentDVR.zip
    sudo chmod +x ./Agent
    msg_ok "Installed AgentDVR"
}

# Function to create systemd service
create_service() {
    msg_info "Creating AgentDVR service"

    sudo bash -c 'cat <<EOF >/etc/systemd/system/AgentDVR.service
[Unit]
Description=AgentDVR Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/agentdvr/agent
ExecStart=/opt/agentdvr/agent/Agent
Environment="MALLOC_TRIM_THRESHOLD_=100000"
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=AgentDVR

[Install]
WantedBy=multi-user.target
EOF'

    # Reload systemd to recognize the new service
    sudo systemctl daemon-reload

    # Enable and start the service
    sudo systemctl enable AgentDVR.service
    sudo systemctl start AgentDVR.service

    # Verify service status
    if systemctl is-active --quiet AgentDVR.service; then
        msg_ok "AgentDVR service created and started successfully"
    else
        msg_error "Failed to start AgentDVR service"
    fi
}

# Function to clean up the system
cleanup_system() {
    msg_info "Cleaning up"
    sudo apt-get -y autoremove
    sudo apt-get -y autoclean
    msg_ok "Cleaned up the system"
}

# Function to display final instructions
final_instructions() {
    echo -e "\n\e[32m[SUCCESS]\e[0m AgentDVR has been installed successfully."
    echo "You can manage the AgentDVR service using the following commands:"
    echo "  sudo systemctl start AgentDVR.service    # Start service"
    echo "  sudo systemctl stop AgentDVR.service     # Stop service"
    echo "  sudo systemctl status AgentDVR.service   # Check service status"
    echo "  sudo systemctl restart AgentDVR.service  # Restart service"
}

# Function to launch Chrome pointing to AgentDVR
launch_chrome() {
    msg_info "Launching Chrome to access AgentDVR"
    # Ensure that WSL can access Windows executables
    if command -v cmd.exe &>/dev/null; then
        cmd.exe /c start chrome http://localhost:8090
        msg_ok "Chrome launched to http://localhost:8090"
    else
        msg_error "cmd.exe not found. Cannot launch Chrome."
    fi
}

# ------------------------------- Main Script ---------------------------------

# Ensure the script is running inside WSL2
if ! is_wsl; then
    msg_error "This script is intended to be run inside WSL2 on Ubuntu 22.04."
fi

# Install dependencies
install_dependencies

# Install AgentDVR
install_agentdvr

# Create and start the AgentDVR service
create_service

# Clean up the system
cleanup_system

# Display final instructions
final_instructions

# Launch Chrome to access AgentDVR
launch_chrome
