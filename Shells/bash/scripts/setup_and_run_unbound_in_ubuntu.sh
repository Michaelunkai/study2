#!/usr/bin/env  

# Name: setup_unbound.sh
# Description: Script to install and configure Unbound on Ubuntu
# Author: wimb0
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
msg_info "Installing Dependencies"
apt-get update && apt-get upgrade -y
apt-get install -y \
    sudo \
    curl \
    mc
msg_ok "Dependencies installed"

# Install Unbound
msg_info "Installing Unbound"
apt-get install -y \
    unbound \
    unbound-host
msg_ok "Unbound installed"

# Configure Unbound
msg_info "Configuring Unbound"
cat <<EOF >/etc/unbound/unbound.conf.d/unbound.conf
server:
  interface: 0.0.0.0
  port: 5335
  do-ip6: no
  hide-identity: yes
  hide-version: yes
  harden-referral-path: yes
  cache-min-ttl: 300
  cache-max-ttl: 14400
  serve-expired: yes
  serve-expired-ttl: 3600
  prefetch: yes
  prefetch-key: yes
  target-fetch-policy: "3 2 1 1 1"
  unwanted-reply-threshold: 10000000
  rrset-cache-size: 256m
  msg-cache-size: 128m
  so-rcvbuf: 1m
  private-address: 192.168.0.0/16
  private-address: 169.254.0.0/16
  private-address: 172.16.0.0/12
  private-address: 10.0.0.0/8
  private-address: fd00::/8
  private-address: fe80::/10
  access-control: 192.168.0.0/16 allow
  access-control: 172.16.0.0/12 allow
  access-control: 10.0.0.0/8 allow
  access-control: 127.0.0.1/32 allow
  chroot: ""
  logfile: /var/log/unbound.log
EOF

touch /var/log/unbound.log
chown unbound:unbound /var/log/unbound.log
systemctl restart unbound
msg_ok "Unbound configured"

# Configure logrotate for Unbound
msg_info "Configuring Logrotate"
cat <<EOF >/etc/logrotate.d/unbound
/var/log/unbound.log {
  daily
  rotate 7
  missingok
  notifempty
  compress
  delaycompress
  sharedscripts
  create 644
  postrotate
    /usr/sbin/unbound-control log_reopen
  endscript
}
EOF

systemctl restart logrotate
msg_ok "Logrotate configured"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with details
msg_info "Unbound setup complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Unbound DNS Resolver is running and listening on port 5335."
echo "To test, configure your DNS resolver to: $IP_ADDRESS:5335"
echo ""
echo "### Unbound: DNS Resolver for Privacy"
echo "A validating, recursive, and caching DNS resolver designed for privacy and speed."
