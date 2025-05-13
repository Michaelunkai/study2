#!/usr/bin/env bash

set -e

# Define helper functions for logging
msg_info() {
  echo -e "\033[1;34m[INFO]\033[0m $1"
}

msg_ok() {
  echo -e "\033[1;32m[OK]\033[0m $1"
}

msg_error() {
  echo -e "\033[1;31m[ERROR]\033[0m $1"
  exit 1
}

# Ensure the script is run as root
if [[ $EUID -ne 0 ]]; then
  msg_error "This script must be run as root. Use sudo."
fi

msg_info "Updating system and installing dependencies"
apt-get update && apt-get upgrade -y
apt-get install -y curl sudo mc apt-transport-https gpg xvfb wget tar
msg_ok "System updated and dependencies installed"

msg_info "Installing Google Chrome"
wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable
msg_ok "Google Chrome installed"

msg_info "Installing FlareSolverr"
RELEASE=$(wget -q https://github.com/FlareSolverr/FlareSolverr/releases/latest -O - | grep "title>Release" | cut -d " " -f 4)
wget -q https://github.com/FlareSolverr/FlareSolverr/releases/download/"$RELEASE"/flaresolverr_linux_x64.tar.gz
tar -xzf flaresolverr_linux_x64.tar.gz -C /opt
rm flaresolverr_linux_x64.tar.gz
echo "$RELEASE" >/opt/flaresolverr_version.txt
msg_ok "FlareSolverr installed"

msg_info "Creating systemd service for FlareSolverr"
cat <<EOF >/etc/systemd/system/flaresolverr.service
[Unit]
Description=FlareSolverr
After=network.target

[Service]
SyslogIdentifier=flaresolverr
Restart=always
RestartSec=5
Type=simple
Environment="LOG_LEVEL=info"
Environment="CAPTCHA_SOLVER=none"
WorkingDirectory=/opt/flaresolverr
ExecStart=/opt/flaresolverr/flaresolverr
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now flaresolverr.service
msg_ok "FlareSolverr service created and started"

msg_info "Cleaning up"
apt-get autoremove -y
apt-get autoclean -y
msg_ok "Cleanup completed"

msg_info "FlareSolverr is running"
echo "Web UI available at: http://localhost:8191"
