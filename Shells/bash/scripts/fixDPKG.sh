#!/bin/bash

############################################################
# fdpkg.sh - A script to repair dpkg and related packages
# Author: Your Name
# Date: YYYY-MM-DD
#
# Description:
# This script repairs the dpkg package management system by
# backing up and resetting the /var/lib/dpkg/info directory,
# updating package lists, reinstalling essential packages,
# adding the i386 architecture, reinstalling Mesa-related packages,
# and performing additional recovery steps.
#
# Usage:
#   sudo ./fdpkg.sh
############################################################

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display messages
echo_msg() {
    echo -e "\n==== $1 ====\n"
}

echo_msg "Starting dpkg repair process..."

# Step 1: Backup and Reset /var/lib/dpkg/info
echo_msg "Backing up /var/lib/dpkg/info..."

if sudo mv /var/lib/dpkg/info /var/lib/dpkg/info_old 2>/dev/null; then
    echo "Moved /var/lib/dpkg/info to /var/lib/dpkg/info_old."
else
    echo "/var/lib/dpkg/info_old already exists. Removing it."
    sudo rm -rf /var/lib/dpkg/info_old
    sudo mv /var/lib/dpkg/info /var/lib/dpkg/info_old
    echo "Moved /var/lib/dpkg/info to /var/lib/dpkg/info_old after removing existing info_old."
fi

# Recreate the info directory
echo_msg "Recreating /var/lib/dpkg/info directory..."
sudo mkdir /var/lib/dpkg/info
sudo chmod 755 /var/lib/dpkg/info
echo "Recreated /var/lib/dpkg/info directory."

# Step 2: Update package lists and reinstall essential packages
echo_msg "Updating package lists..."
sudo apt-get update -y
echo "Package lists updated."

echo_msg "Reinstalling dpkg and apt..."
sudo apt-get install --reinstall -y dpkg apt
echo "Reinstalled dpkg and apt."

# Step 3: Add i386 architecture and reinstall Mesa packages
echo_msg "Adding i386 architecture..."
sudo dpkg --add-architecture i386
echo "i386 architecture added."

echo_msg "Updating package lists after adding i386 architecture..."
sudo apt-get update -y
echo "Package lists updated."

echo_msg "Reinstalling Mesa-related packages..."
sudo apt-get install --reinstall -y libgl1-mesa-glx libglx-mesa0 libgl1-mesa-dri mesa-vulkan-drivers libgl1-mesa-dri:i386
echo "Reinstalled Mesa-related packages."

echo_msg "Setting permissions for /run/user/$(id -u)..."
sudo chmod 0700 /run/user/$(id -u)
echo "Permissions set."

# Optional Step 4: Additional Recovery Steps
echo_msg "Performing additional recovery steps..."

echo_msg "Reconfiguring all partially installed packages..."
sudo dpkg --configure -a
echo "Reconfigured packages."

echo_msg "Fixing broken dependencies..."
sudo apt-get install -f -y
echo "Fixed broken dependencies."

echo_msg "Cleaning package caches..."
sudo apt-get clean
sudo apt-get autoclean
echo "Package caches cleaned."

echo_msg "Removing unnecessary packages..."
sudo apt-get autoremove -y
echo "Unnecessary packages removed."

# Uncomment the following lines if you want to reinstall all installed packages
# echo_msg "Reinstalling all installed packages..."
# sudo apt-get install --reinstall -y $(dpkg --get-selections | grep install | awk '{print $1}')
# echo "Reinstalled all installed packages."

echo_msg "dpkg repair process completed successfully."
