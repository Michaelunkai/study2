#!/usr/bin/env bash

# Script to install and configure Apt-Cacher NG on Ubuntu 22 WSL2

# Functions to display messages
msg_info() {
    echo -e "\e[34m[INFO]\e[0m $1"
}

msg_ok() {
    echo -e "\e[32m[OK]\e[0m $1"
}

msg_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
}

# Update package list
msg_info "Updating package list"
sudo apt-get update
msg_ok "Package list updated"

# Install Dependencies
msg_info "Installing Dependencies"
sudo apt-get install -y curl sudo mc
msg_ok "Installed Dependencies"

# Install Apt-Cacher NG
msg_info "Installing Apt-Cacher NG"
DEBIAN_FRONTEND=noninteractive sudo apt-get -o Dpkg::Options::="--force-confold" install -y apt-cacher-ng
msg_ok "Installed Apt-Cacher NG"

# Configure Apt-Cacher NG
msg_info "Configuring Apt-Cacher NG"
sudo sed -i 's|# PassThroughPattern: \.\* # this would allow CONNECT to everything|PassThroughPattern: .*|' /etc/apt-cacher-ng/acng.conf
msg_ok "Configured Apt-Cacher NG"

# Enable and start the service
msg_info "Starting Apt-Cacher NG service"
sudo systemctl enable --now apt-cacher-ng
msg_ok "Apt-Cacher NG service started"

# Cleaning up
msg_info "Cleaning up"
sudo apt-get -y autoremove
sudo apt-get -y autoclean
msg_ok "Cleaned up"

# Echo the URL for the web UI
echo ""
msg_ok "Apt-Cacher NG is running."
echo "Access the web UI at: http://localhost:3142/acng-report.html"
