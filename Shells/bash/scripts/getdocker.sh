#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Suppress prompts during package installation
export DEBIAN_FRONTEND=noninteractive

# Function to display informational messages
echo_info() {
    echo -e "\e[32m[INFO]\e[0m $1"
}

# Function to display error messages
echo_error() {
    echo -e "\e[31m[ERROR]\e[0m $1" >&2
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to cleanup existing Docker installations
cleanup_docker() {
    echo_info "Removing any existing Docker installations..."
    sudo systemctl stop docker || true
    sudo systemctl disable docker || true
    sudo umount /var/lib/docker/* || true
    sudo apt-get remove -y docker docker-engine docker.io containerd runc docker-ce docker-ce-cli docker-buildx-plugin docker-compose-plugin || true
    sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin || true
    sudo rm -rf /var/lib/docker || true
    sudo rm -rf /etc/docker || true
    sudo rm -f /usr/local/bin/docker-compose
    sudo rm -f /usr/bin/docker-compose
    sudo rm -f /usr/libexec/docker/cli-plugins/docker-compose
    sudo rm -f /etc/apt/sources.list.d/docker.list
    sudo rm -rf /etc/apt/keyrings/docker.gpg
    echo_info "Cleanup complete."
}

# Function to fix /usr/bin/docker issue
fix_docker_binary() {
    echo_info "Fixing /usr/bin/docker issue..."
    if [ ! -f /usr/bin/docker ]; then
        sudo ln -s /usr/libexec/docker/cli-plugins/docker /usr/bin/docker || true
    fi
}

# Step 1: Cleanup Existing Docker Installations
cleanup_docker

# Step 2: Update Package Index
echo_info "Updating package index..."
sudo apt-get update -y

# Step 3: Install Prerequisite Packages
echo_info "Installing prerequisite packages..."
sudo apt-get install -y ca-certificates curl gnupg lsb-release acl

# Step 4: Add Docker’s Official GPG Key
echo_info "Adding Docker's GPG key..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Verify that the GPG key was added successfully
if [ ! -f /etc/apt/keyrings/docker.gpg ]; then
    echo_error "Failed to add Docker GPG key."
    exit 1
fi

# Step 5: Set Up the Docker Repository for Ubuntu Jammy
echo_info "Setting up the Docker repository for Ubuntu Jammy..."
UBUNTU_CODENAME=$(lsb_release -cs)
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $UBUNTU_CODENAME stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Step 6: Update Package Index with Docker Packages
echo_info "Updating package index with Docker packages..."
sudo apt install docker-compose -y
sudo apt-get update -y

# Step 7: Install Docker Engine and Related Components
echo_info "Installing Docker Engine and related components..."
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Step 8: Verify Docker Installation
echo_info "Verifying Docker installation..."
if ! command_exists docker; then
    echo_error "Docker installation failed. 'docker' command not found."
    exit 1
fi
echo "Docker version: $(docker --version)"

# Step 9: Fix /usr/bin/docker Issue
fix_docker_binary

# Step 10: Start and Enable Docker Service
echo_info "Starting and enabling Docker service..."
sudo systemctl daemon-reload
sudo systemctl start docker
sudo systemctl enable docker

# Step 11: Add Current User to the 'docker' Group
echo_info "Adding user '$USER' to the 'docker' group..."
sudo groupadd docker 2>/dev/null || true
sudo usermod -aG docker "$USER"

# Step 12: Verify Docker Service
echo_info "Verifying Docker service status..."
if ! sudo systemctl is-active --quiet docker; then
    echo_error "Docker service failed to start."
    exit 1
fi
echo_info "Docker service is active and running."

# Step 13: Final Message
echo_info "Docker installation complete. Please log out and log back in for the group changes to take effect."
