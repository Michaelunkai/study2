#!/usr/bin/env bash

# Script to install CasaOS on a Debian-based system
# License: MIT
# https://github.com/IceWhaleTech/CasaOS

set -e

# Define colors for logging
GREEN="\e[32m"
YELLOW="\e[33m"
RED="\e[31m"
RESET="\e[0m"

log_info() {
    echo -e "${YELLOW}[INFO]${RESET} $1"
}

log_ok() {
    echo -e "${GREEN}[OK]${RESET} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${RESET} $1"
    exit 1
}

# Function to update the system and install dependencies
install_dependencies() {
    log_info "Updating package lists..."
    apt-get update -y || log_error "Failed to update package lists"

    log_info "Installing required packages..."
    apt-get install -y curl sudo mc || log_error "Failed to install dependencies"
    log_ok "Dependencies installed successfully"
}

# Function to install CasaOS
install_casaos() {
    log_info "Installing CasaOS..."
    DOCKER_CONFIG_PATH='/etc/docker/daemon.json'
    mkdir -p "$(dirname $DOCKER_CONFIG_PATH)"
    echo -e '{\n  "log-driver": "journald"\n}' > "$DOCKER_CONFIG_PATH"
    bash <(curl -fsSL https://get.casaos.io/v0.4.1) || log_error "CasaOS installation failed"
    log_ok "CasaOS installed successfully"
}

# Function to clean up unnecessary packages
clean_up() {
    log_info "Cleaning up..."
    apt-get -y autoremove || log_error "Failed to autoremove packages"
    apt-get -y autoclean || log_error "Failed to clean up packages"
    log_ok "System cleaned up"
}

# Function to display CasaOS URL
display_access_url() {
    IP_ADDRESS=$(hostname -I | awk '{print $1}')
    log_ok "CasaOS installation completed. Access it in your browser."
    echo -e "${GREEN}[INFO]${RESET} CasaOS is running at: http://${IP_ADDRESS}"
}

# Main script execution
log_info "Starting CasaOS installation script"
install_dependencies
install_casaos
clean_up
display_access_url
