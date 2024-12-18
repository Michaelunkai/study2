#!/usr/bin/env bash

# Tool: Cloudflared Installer
# Purpose: Install and configure Cloudflared for DNS-over-HTTPS (DoH) or web tunneling.
# Author: tteck (tteckster)
# License: MIT

set -e

# Color Functions for Info and Error Messages
msg_info() {
  echo -e "\e[34m[INFO]\e[0m $1"
}
msg_ok() {
  echo -e "\e[32m[OK]\e[0m $1"
}
msg_error() {
  echo -e "\e[31m[ERROR]\e[0m $1" >&2
}

# Update OS and Check for Dependencies
msg_info "Updating OS and Installing Dependencies"
sudo apt-get update
sudo apt-get install -y curl sudo mc
msg_ok "Dependencies Installed"

# Install Cloudflared
msg_info "Installing Cloudflared"
mkdir -p --mode=0755 /usr/share/keyrings
VERSION="$(awk -F'=' '/^VERSION_CODENAME=/{ print $NF }' /etc/os-release)"
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg >/usr/share/keyrings/cloudflare-main.gpg
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $VERSION main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt-get update
sudo apt-get install -y cloudflared
msg_ok "Cloudflared Installed"

# Prompt for DNS-over-HTTPS Configuration
read -r -p "Configure Cloudflared as a DNS-over-HTTPS (DoH) proxy? <y/N>: " prompt
if [[ ${prompt,,} =~ ^(y|yes)$ ]]; then
  msg_info "Configuring DNS-over-HTTPS (DoH)"
  
  # Create Configuration File
  sudo mkdir -p /usr/local/etc/cloudflared
  cat <<EOF | sudo tee /usr/local/etc/cloudflared/config.yml
proxy-dns: true
proxy-dns-address: 0.0.0.0
proxy-dns-port: 53
proxy-dns-max-upstream-conns: 5
proxy-dns-upstream:
  - https://1.1.1.1/dns-query
  - https://1.0.0.1/dns-query
EOF

  # Create Systemd Service
  cat <<EOF | sudo tee /etc/systemd/system/cloudflared.service
[Unit]
Description=Cloudflared DNS-over-HTTPS (DoH) Proxy
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/cloudflared --config /usr/local/etc/cloudflared/config.yml
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

  # Enable and Start Service
  sudo systemctl enable --now cloudflared.service
  msg_ok "DNS-over-HTTPS Configured and Service Started"
fi

# Clean Up
msg_info "Cleaning Up"
sudo apt-get autoremove -y
sudo apt-get autoclean -y
msg_ok "Clean-Up Complete"

# Start Cloudflared Tunnel
msg_info "Starting Cloudflared Tunnel for Web UI"
cloudflared tunnel login
cloudflared tunnel create webui-tunnel
CNAME_URL=$(cloudflared tunnel route dns webui-tunnel | grep -Eo "https://.*")
msg_ok "Cloudflared Tunnel Started"

# Echo WebUI URL
echo -e "\n\e[32mWebUI URL: $CNAME_URL\e[0m"
