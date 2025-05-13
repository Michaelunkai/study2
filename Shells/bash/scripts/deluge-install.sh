#!/usr/bin/env bash

# Install Deluge in Ubuntu 22.04 on WSL2
# Script author: tteck (tteckster)
# Adapted for Ubuntu 22.04 WSL2 by AI
# License: MIT
# https://github.com/community-scripts/ProxmoxVE/raw/main/LICENSE

set -e  # Exit on error

# Functions for colored output
msg_info() { echo -e "\e[34m[INFO]\e[0m $1"; }
msg_ok() { echo -e "\e[32m[OK]\e[0m $1"; }
msg_error() { echo -e "\e[31m[ERROR]\e[0m $1"; }

# Ensure script is run with sudo
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" >&2
  exit 1
fi

# Variables
DELUGE_WEB_UI_PORT=8112
DELUGE_DEFAULT_PASSWORD="deluge"

msg_info "Updating system and installing dependencies"
apt-get update -y && apt-get upgrade -y
apt-get install -y curl sudo mc python3-libtorrent python3 python3-dev python3-pip
msg_ok "System updated and dependencies installed"

msg_info "Installing Deluge"
pip install deluge[all]
msg_ok "Deluge installed"

msg_info "Creating systemd services for Deluge"
# Deluged service
cat <<EOF >/etc/systemd/system/deluged.service
[Unit]
Description=Deluge Bittorrent Client Daemon
After=network-online.target

[Service]
Type=simple
UMask=007
ExecStart=/usr/local/bin/deluged -d
Restart=on-failure
TimeoutStopSec=300

[Install]
WantedBy=multi-user.target
EOF

# Deluge Web service
cat <<EOF >/etc/systemd/system/deluge-web.service
[Unit]
Description=Deluge Bittorrent Client Web Interface
After=deluged.service
Wants=deluged.service

[Service]
Type=simple
UMask=027
ExecStart=/usr/local/bin/deluge-web -d
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services
systemctl enable --now deluged.service
systemctl enable --now deluge-web.service
msg_ok "Deluge services created and started"

msg_info "Configuring Deluge Web UI password"
# Ensure config directory exists
mkdir -p /root/.config/deluge

# Create or update auth file for Deluge
AUTH_FILE="/root/.config/deluge/auth"
if ! grep -q "^localclient:" $AUTH_FILE 2>/dev/null; then
  echo "localclient:localclient:10" >>$AUTH_FILE
fi

# Update web.conf to include default password
WEB_CONF="/root/.config/deluge/web.conf"
if [[ -f $WEB_CONF ]]; then
  sed -i "s/\"pwd_.*\"/\"pwd_sha1\":\"$(echo -n $DELUGE_DEFAULT_PASSWORD | sha1sum | awk '{print $1}')\"/" $WEB_CONF
else
  cat <<EOF >$WEB_CONF
{
  "file": 1,
  "format": 1,
  "pwd_sha1": "$(echo -n $DELUGE_DEFAULT_PASSWORD | sha1sum | awk '{print $1}')",
  "port": $DELUGE_WEB_UI_PORT
}
EOF
fi
msg_ok "Web UI password configured"

msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Output WebUI URL and password
msg_ok "Deluge installation completed"
echo "Access the Deluge Web UI at: http://<your-ip>:$DELUGE_WEB_UI_PORT"
echo "Default password: $DELUGE_DEFAULT_PASSWORD"
