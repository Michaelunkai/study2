#!/usr/bin/env  

# Name: setup_notifiarr.sh
# Description: Script to install Notifiarr on Ubuntu
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
    gpg
msg_ok "Dependencies installed"

# Install Notifiarr
msg_info "Installing Notifiarr"
groupadd notifiarr || true
useradd -g notifiarr notifiarr || true
wget -qO- https://packagecloud.io/golift/pkgs/gpgkey | gpg --dearmor >/usr/share/keyrings/golift-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/golift-archive-keyring.gpg] https://packagecloud.io/golift/pkgs/ubuntu focal main" >/etc/apt/sources.list.d/golift.list
apt-get update
apt-get install -y notifiarr
msg_ok "Notifiarr installed"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with instructions
msg_info "Notifiarr installation complete"
echo "To configure Notifiarr, edit the configuration file at: /etc/notifiarr/notifiarr.conf"
echo "Start the service with: sudo systemctl start notifiarr"
echo "Check the service status with: sudo systemctl status notifiarr"
