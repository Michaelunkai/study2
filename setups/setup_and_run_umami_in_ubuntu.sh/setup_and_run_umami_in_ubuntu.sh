#!/usr/bin/env  

# Name: setup_umami.sh
# Description: Script to install Umami on Ubuntu
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
msg_info "Installing Dependencies"
apt-get update && apt-get upgrade -y
apt-get install -y \
    curl \
    sudo \
    mc \
    git \
    gpg \
    postgre 
msg_ok "Dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js Repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
apt-get update
msg_ok "Node.js Repository set up"

# Install Node.js
msg_info "Installing Node.js"
apt-get install -y nodejs
npm install -g yarn
msg_ok "Node.js installed"

# Set up PostgreSQL
msg_info "Setting up PostgreSQL"
DB_NAME=umamidb
DB_USER=umami
DB_PASS=$(openssl rand -base64 18 | tr -dc 'a-zA-Z0-9' | head -c13)
SECRET_KEY="$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32)"

sudo -u postgres psql -c "CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME WITH OWNER $DB_USER ENCODING 'UTF8' TEMPLATE template0;"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC'"

cat <<EOF >~/umami.creds
Umami Database Credentials

Database User: $DB_USER
Database Password: $DB_PASS
Database Name: $DB_NAME
EOF
msg_ok "PostgreSQL configured"

# Install Umami
msg_info "Installing Umami (Patience)"
git clone -q https://github.com/umami-software/umami.git /opt/umami
cd /opt/umami
yarn install
cat <<EOF > /opt/umami/.env
DATABASE_URL=postgre ://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME
EOF
yarn run build
msg_ok "Umami installed"

# Create systemd service
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/umami.service
[Unit]
Description=Umami - Simple Analytics
After=network.target

[Service]
Type=simple
Restart=always
User=root
WorkingDirectory=/opt/umami
ExecStart=/usr/bin/yarn run start

[Install]
WantedBy=multi-user.target
EOF
systemctl enable --now umami.service
msg_ok "Service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Umami installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Umami is running and accessible at: http://$IP_ADDRESS:3000"
echo ""
echo "### Umami: Simple Privacy-Focused Analytics"
echo "A lightweight and privacy-friendly web analytics solution for your websites."
