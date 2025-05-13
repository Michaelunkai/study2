#!/usr/bin/env  

# Name: setup_zipline.sh
# Description: Script to install Zipline on Ubuntu
# Author: tteck
# Co-Author: MickLesk (Canbiz)
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
apt-get update && apt-get install -y \
    postgre  \
    gpg \
    curl \
    sudo \
    mc
msg_ok "Dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js Repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
msg_ok "Node.js repository set up"

# Install Node.js
msg_info "Installing Node.js"
apt-get update && apt-get install -y nodejs
npm install -g yarn
msg_ok "Node.js installed"

# Set up PostgreSQL database
msg_info "Setting up PostgreSQL"
DB_NAME=ziplinedb
DB_USER=zipline
DB_PASS="$(openssl rand -base64 18 | tr -dc 'a-zA-Z0-9' | cut -c1-13)"
SECRET_KEY="$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | cut -c1-13)"
sudo -u postgres psql -c "CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME WITH OWNER $DB_USER ENCODING 'UTF8' TEMPLATE template0;"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC'"
{
    echo "Zipline Database User: $DB_USER"
    echo "Zipline Database Password: $DB_PASS"
    echo "Zipline Database Name: $DB_NAME"
    echo "Zipline Secret Key: $SECRET_KEY"
} > ~/zipline.creds
msg_ok "PostgreSQL set up"

# Install Zipline
msg_info "Installing Zipline (Patience)"
cd /opt
RELEASE=$(curl -s https://api.github.com/repos/diced/zipline/releases/latest | grep "tag_name" | awk '{print substr($2, 3, length($2)-4) }')
wget -q "https://github.com/diced/zipline/archive/refs/tags/v${RELEASE}.zip"
unzip -q v${RELEASE}.zip
mv zipline-${RELEASE} /opt/zipline
cd /opt/zipline
mv .env.local.example .env
sed -i "s|CORE_SECRET=.*|CORE_SECRET=\"$SECRET_KEY\"|" .env
sed -i "s|CORE_RETURN_HTTPS=.*|CORE_RETURN_HTTPS=false|" .env
sed -i "s|CORE_DATABASE_URL=.*|CORE_DATABASE_URL=\"postgres://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME\"|" .env
yarn install
yarn build
echo "${RELEASE}" > /opt/zipline_version.txt
msg_ok "Zipline installed"

# Create systemd service
msg_info "Creating Service"
cat <<EOF >/etc/systemd/system/zipline.service
[Unit]
Description=Zipline Service
After=network.target

[Service]
WorkingDirectory=/opt/zipline
ExecStart=/usr/bin/yarn start
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now zipline.service
msg_ok "Service created"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display URL and tool explanation
msg_info "Zipline installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Zipline is running and accessible at: http://$IP_ADDRESS:3000"
echo ""
echo "### Zipline: Lightweight File Hosting Platform"
echo "Efficient, self-hosted file-sharing solution."
