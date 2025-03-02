#!/usr/bin/env  

# Script for installing Channels DVR Server on Ubuntu 22 (WSL2 compatible)

# Ensure the script exits on errors
set -e

echo "Updating package list and upgrading installed packages..."
sudo apt-get update
sudo apt-get upgrade -y

echo "Installing dependencies..."
sudo apt-get install -y curl sudo mc xvfb

echo "Installing Google Chrome and dependencies..."
cd ~
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
sudo apt install -y chromium-chromedriver
sudo apt-get install -y libnss3 libgconf-2-4

# Optional hardware acceleration setup
if [[ "$(grep -Ei 'microsoft.*wsl' /proc/version)" ]]; then
  echo "WSL2 detected. Skipping hardware acceleration setup."
else
  echo "Setting up hardware acceleration..."
  sudo apt-get install -y va-driver-all ocl-icd-libopencl1 intel-opencl-icd
  sudo chgrp video /dev/dri
  sudo chmod 755 /dev/dri
  sudo chmod 660 /dev/dri/*
  sudo usermod -aG video $(whoami)
  sudo usermod -aG render $(whoami)
  echo "Hardware acceleration setup completed."
fi

echo "Installing Channels DVR Server..."
cd /opt
curl -fsSL https://getchannels.com/dvr/setup.sh | sudo bash

echo "Adjusting user group permissions..."
sudo sed -i -e 's/^sgx:x:104:$/render:x:104:root/' -e 's/^render:x:106:root$/sgx:x:106:/' /etc/group

echo "Cleaning up unnecessary packages..."
sudo apt-get autoremove -y
sudo apt-get autoclean -y

echo "Installation completed successfully!"
echo "You can access the Channels DVR Server WebUI at: http://localhost:8089"
