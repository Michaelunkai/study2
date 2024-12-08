#!/usr/bin/env bash

# Script to install ArchiveBox on Ubuntu 22 in WSL2

# Function to check if systemd is running
check_systemd() {
    if pidof systemd >/dev/null; then
        echo "Systemd is running."
        USE_SYSTEMD=1
    else
        echo "Systemd is not running."
        USE_SYSTEMD=0
    fi
}

# Update the package list
echo "Updating package list..."
sudo apt-get update

# Install Dependencies
echo "Installing dependencies..."
sudo apt-get install -y \
  curl \
  sudo \
  mc \
  git \
  expect \
  libssl-dev \
  libldap2-dev \
  libsasl2-dev \
  procps \
  dnsutils \
  ripgrep

# Install Python Dependencies
echo "Installing Python dependencies..."
sudo apt-get install -y \
  python3-pip \
  python3-ldap \
  python3-msgpack \
  python3-regex

# Set up Node.js Repository
echo "Setting up Node.js repository..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/nodesource.list

# Install Node.js
echo "Installing Node.js..."
sudo apt-get update
sudo apt-get install -y nodejs

# Install Playwright and Chromium
echo "Installing Playwright and Chromium..."
sudo pip3 install playwright
sudo playwright install --with-deps chromium

# Install ArchiveBox
echo "Installing ArchiveBox..."
sudo mkdir -p /opt/archivebox/{data,.npm,.cache,.local}
sudo adduser --system --shell /bin/bash --gecos 'Archive Box User' --group --disabled-password archivebox
sudo chown -R archivebox:archivebox /opt/archivebox/{data,.npm,.cache,.local}
sudo chmod -R 755 /opt/archivebox/data
sudo pip3 install archivebox

# Set up ArchiveBox
echo "Setting up ArchiveBox..."
cd /opt/archivebox/data
sudo -u archivebox archivebox setup <<EOF
admin
admin@example.com
yourpassword
yourpassword
EOF

# Check if systemd is running
check_systemd

if [ "$USE_SYSTEMD" -eq 1 ]; then
    # Create Systemd Service
    echo "Creating systemd service..."
    sudo bash -c 'cat <<EOF >/etc/systemd/system/archivebox.service
[Unit]
Description=ArchiveBox Server
After=network.target

[Service]
User=archivebox
WorkingDirectory=/opt/archivebox/data
ExecStart=/usr/local/bin/archivebox server 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

    sudo systemctl daemon-reload
    sudo systemctl enable --now archivebox.service

    echo "ArchiveBox is installed and running."
    echo "You can access the web UI at: http://localhost:8000"

else
    # Start the ArchiveBox server manually
    echo "Starting ArchiveBox server in the background..."
    sudo -u archivebox nohup archivebox server 0.0.0.0:8000 >/dev/null 2>&1 &
    echo "ArchiveBox is installed and running."
    echo "You can access the web UI at: http://localhost:8000"
    echo "Note: The server is running in the background and will stop when you close the terminal."
fi

# Clean up
echo "Cleaning up..."
sudo apt-get -y autoremove
sudo apt-get -y autoclean
