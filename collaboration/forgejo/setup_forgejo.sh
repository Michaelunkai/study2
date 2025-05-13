#!/usr/bin/env  

# Script for installing Forgejo on Ubuntu 22 WSL2
# Updated and streamlined for WSL2 by ChatGPT
# License: MIT

set -e

# Define helper functions for colored output
msg_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
msg_ok() { echo -e "\033[1;32m[OK]\033[0m $1"; }

# Update system and install dependencies
msg_info "Updating and Installing Dependencies"
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl sudo mc git git-lfs
msg_ok "Dependencies Installed"

# Install Forgejo
msg_info "Installing Forgejo"
mkdir -p /opt/forgejo
RELEASE=$(curl -s https://codeberg.org/api/v1/repos/forgejo/forgejo/releases/latest | grep -oP '"tag_name":\s*"\K[^"]+' | sed 's/^v//')
wget -qO /opt/forgejo/forgejo-$RELEASE-linux-amd64 "https://codeberg.org/forgejo/forgejo/releases/download/v${RELEASE}/forgejo-${RELEASE}-linux-amd64"
chmod +x /opt/forgejo/forgejo-$RELEASE-linux-amd64
sudo ln -sf /opt/forgejo/forgejo-$RELEASE-linux-amd64 /usr/local/bin/forgejo
msg_ok "Forgejo Installed"

# Set up Forgejo user and directories
msg_info "Setting Up Forgejo"
sudo adduser --system --shell /bin/bash --gecos 'Git Version Control' --group --disabled-password --home /home/git git || true
sudo mkdir -p /var/lib/forgejo /etc/forgejo
sudo chown -R git:git /var/lib/forgejo
sudo chmod 750 /var/lib/forgejo
sudo chown root:git /etc/forgejo
sudo chmod 770 /etc/forgejo
msg_ok "Forgejo Setup Complete"

# Create systemd service
msg_info "Creating Service"
cat <<EOF | sudo tee /etc/systemd/system/forgejo.service > /dev/null
[Unit]
Description=Forgejo
After=syslog.target
After=network.target
[Service]
RestartSec=2s
Type=simple
User=git
Group=git
WorkingDirectory=/var/lib/forgejo/
ExecStart=/usr/local/bin/forgejo web --config /etc/forgejo/app.ini
Restart=always
Environment=USER=git HOME=/home/git GITEA_WORK_DIR=/var/lib/forgejo
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable --now forgejo
msg_ok "Service Created and Started"

# Clean up
msg_info "Cleaning Up"
sudo apt-get -y autoremove
sudo apt-get -y autoclean
msg_ok "Clean Up Complete"

# Display Web UI URL
msg_info "Forgejo Installation Complete"
echo -e "Forgejo WebUI is running. Access it at: http://localhost:3000"
