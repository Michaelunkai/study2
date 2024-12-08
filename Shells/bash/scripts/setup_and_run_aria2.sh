#!/usr/bin/env bash

# Author: Updated by Assistant
# License: MIT
# Compatibility: Ubuntu 22.04 on WSL2

set -e

# Define helper functions
msg_info() { echo -e "\e[34m[INFO]\e[0m $1"; }
msg_ok() { echo -e "\e[32m[OK]\e[0m $1"; }
msg_error() { echo -e "\e[31m[ERROR]\e[0m $1"; exit 1; }

# Update and install dependencies
msg_info "Updating system and installing dependencies"
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y curl sudo mc aria2 nginx unzip openssl
msg_ok "Dependencies installed"

# Set up Aria2
msg_info "Configuring Aria2"
mkdir -p /root/downloads
rpc_secret=$(openssl rand -base64 12)
echo "rpc-secret: $rpc_secret" > /root/aria2.daemon
cat <<EOF >>/root/aria2.daemon
dir=/root/downloads
file-allocation=falloc
max-connection-per-server=4
max-concurrent-downloads=2
max-overall-download-limit=0
min-split-size=25M
rpc-allow-origin-all=true
input-file=/var/tmp/aria2c.session
save-session=/var/tmp/aria2c.session
EOF

# Create systemd service for Aria2
cat <<EOF | sudo tee /etc/systemd/system/aria2.service > /dev/null
[Unit]
Description=Aria2 download manager
After=network.target

[Service]
Type=simple
User=root
ExecStartPre=/usr/bin/env touch /var/tmp/aria2c.session
ExecStart=/usr/bin/aria2c --enable-rpc --rpc-listen-all --conf-path=/root/aria2.daemon
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable --now aria2.service
msg_ok "Aria2 configured and started"

# Set up AriaNG
read -r -p "Would you like to install AriaNG Web UI? (y/N): " prompt
if [[ ${prompt,,} =~ ^(y|yes)$ ]]; then
    msg_info "Installing AriaNG"
    latest_release=$(curl -s https://api.github.com/repos/mayswind/ariang/releases/latest | grep browser_download_url | grep AllInOne.zip | cut -d\" -f4)
    wget -q "$latest_release" -O AriaNg.zip
    sudo unzip -o AriaNg.zip -d /var/www/ariang
    rm AriaNg.zip
    sudo rm -f /etc/nginx/sites-enabled/default
    cat <<EOF | sudo tee /etc/nginx/conf.d/ariang.conf > /dev/null
server {
    listen 6880 default_server;
    listen [::]:6880 default_server;

    server_name _;

    root /var/www/ariang;
    index index.html;

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF
    sudo systemctl restart nginx
    msg_ok "AriaNG installed and available at http://localhost:6880"
fi

# Final cleanup
msg_info "Performing cleanup"
sudo apt-get autoremove -y
sudo apt-get autoclean -y
msg_ok "Cleanup completed"

# Display final information
msg_ok "Aria2 and Web UI setup complete!"
echo -e "Access Aria2 Web UI at: \e[32mhttp://localhost:6880\e[0m"
echo -e "RPC Secret: \e[32m$rpc_secret\e[0m"
