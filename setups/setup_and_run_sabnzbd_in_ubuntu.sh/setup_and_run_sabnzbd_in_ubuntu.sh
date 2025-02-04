#!/usr/bin/env  

# Name: setup_sabnzbd.sh
# Description: Script to install SABnzbd on Ubuntu
# Author: tteck
# License: MIT

# Exit immediately if a command exits with a non-zero status
set -e

# Functions for colored output
function msg_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

function msg_ok() {
    echo -e "\033[1;32m[OK]\033[0m $1"
}

function msg_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
    exit 1
}

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    msg_error "This script must be run as root or with sudo"
fi

# Install dependencies
msg_info "Installing dependencies"
apt-get update && apt-get install -y \
    curl \
    sudo \
    mc \
    par2 \
    p7zip-full \
     3-dev \
     3-pip \
     3-setuptools
cat <<EOF >/etc/apt/sources.list.d/non-free.list
deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
EOF
apt-get update && apt-get install -y unrar
rm /etc/apt/sources.list.d/non-free.list
msg_ok "Dependencies installed"

# Update Python3
msg_info "Updating Python3"
rm -rf /usr/lib/ 3.*/EXTERNALLY-MANAGED
msg_ok "Python3 updated"

# Install SABnzbd
msg_info "Installing SABnzbd"
RELEASE=$(curl -s https://api.github.com/repos/sabnzbd/sabnzbd/releases/latest | grep "tag_name" | awk '{print substr($2, 2, length($2)-3) }')
tar zxvf <(curl -fsSL https://github.com/sabnzbd/sabnzbd/releases/download/$RELEASE/SABnzbd-${RELEASE}-src.tar.gz) -C /opt
mv /opt/SABnzbd-${RELEASE} /opt/sabnzbd
cd /opt/sabnzbd
python3 -m pip install -r requirements.txt
msg_ok "SABnzbd installed"

# Create and enable SABnzbd service
msg_info "Creating SABnzbd service"
cat <<EOF >/etc/systemd/system/sabnzbd.service
[Unit]
Description=SABnzbd
After=network.target

[Service]
WorkingDirectory=/opt/sabnzbd
ExecStart=/usr/bin/python3 SABnzbd.py -s 0.0.0.0:7777
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now sabnzbd.service
msg_ok "SABnzbd service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "SABnzbd installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "SABnzbd is running and accessible at: http://$IP_ADDRESS:7777"
echo "Use the web interface to complete the setup."
