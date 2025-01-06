#!/usr/bin/env  

# Updated for Ubuntu 22 WSL2
# Original Author: tteck
# License: MIT
# Repository: https://github.com/0xERR0R/blocky

# Define helper functions
function msg_info {
    echo -e "\e[94m[INFO] $1\e[0m"
}

function msg_ok {
    echo -e "\e[92m[OK] $1\e[0m"
}

function msg_error {
    echo -e "\e[91m[ERROR] $1\e[0m"
    exit 1
}

# Ensure script runs as root
if [[ $EUID -ne 0 ]]; then
   msg_error "This script must be run as root."
fi

# Update and install dependencies
msg_info "Updating package list and installing dependencies"
apt-get update -y
apt-get install -y curl sudo mc || msg_error "Failed to install dependencies"
msg_ok "Dependencies installed"

# Disable systemd-resolved if running
msg_info "Disabling systemd-resolved if active"
if systemctl is-active systemd-resolved > /dev/null 2>&1; then
  systemctl disable --now systemd-resolved || msg_error "Failed to disable systemd-resolved"
fi
msg_ok "systemd-resolved disabled"

# Install Blocky
msg_info "Installing Blocky"
mkdir -p /opt/blocky
RELEASE=$(curl -s https://api.github.com/repos/0xERR0R/blocky/releases/latest | grep "tag_name" | awk -F '"' '{print $4}')
curl -sL "https://github.com/0xERR0R/blocky/releases/download/${RELEASE}/blocky_${RELEASE}_Linux_x86_64.tar.gz" | tar -xzf - -C /opt/blocky || msg_error "Failed to install Blocky"
msg_ok "Blocky installed"

# Configure Blocky
msg_info "Configuring Blocky"
cat <<EOF >/opt/blocky/config.yml
upstream:
  default:
    - 1.1.1.1
blocking:
  blackLists:
    ads:
      - https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
  blockType: zeroIp
port: 553
EOF
msg_ok "Configuration file created"

# Create Systemd service
msg_info "Creating Blocky service"
cat <<EOF >/etc/systemd/system/blocky.service
[Unit]
Description=Blocky
After=network.target
[Service]
User=root
WorkingDirectory=/opt/blocky
ExecStart=/opt/blocky/blocky --config config.yml
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl enable --now blocky || msg_error "Failed to enable and start Blocky"
msg_ok "Blocky service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y
apt-get autoclean -y
msg_ok "Cleanup complete"

# Echo URL for WebUI
msg_info "Setup complete. Blocky is running."
echo -e "\e[92mAccess Blocky DNS at: http://127.0.0.1:553\e[0m"
