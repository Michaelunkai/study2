#!/usr/bin/env  

# Name: setup_netbox.sh
# Description: Script to install NetBox on Ubuntu
# Author: bvdberg01
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
    curl \
    sudo \
    mc \
    apache2 \
    redis-server \
    postgre  \
     3 \
     3-pip \
     3-venv \
     3-dev \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    zlib1g-dev
msg_ok "Installed Dependencies"

# Set up PostgreSQL
msg_info "Setting up PostgreSQL"
DB_NAME=netbox
DB_USER=netbox
DB_PASS=$(openssl rand -base64 18 | tr -dc 'a-zA-Z0-9' | cut -c1-13)

sudo -u postgres psql -c "CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME WITH OWNER $DB_USER TEMPLATE template0;"

{
echo "Netbox-Credentials"
echo -e "Netbox Database User: \e[32m$DB_USER\e[0m"
echo -e "Netbox Database Password: \e[32m$DB_PASS\e[0m"
echo -e "Netbox Database Name: \e[32m$DB_NAME\e[0m"
} >> ~/netbox.creds
msg_ok "Set up PostgreSQL"

# Install NetBox
msg_info "Installing NetBox (Patience)"
cd /opt
RELEASE=$(curl -s https://api.github.com/repos/netbox-community/netbox/releases/latest | grep "tag_name" | awk '{print substr($2, 3, length($2)-4) }')
wget -q "https://github.com/netbox-community/netbox/archive/refs/tags/v${RELEASE}.zip"
unzip -q "v${RELEASE}.zip"
mv /opt/netbox-${RELEASE}/ /opt/netbox

adduser --system --group netbox
chown --recursive netbox /opt/netbox/netbox/media/
chown --recursive netbox /opt/netbox/netbox/reports/
chown --recursive netbox /opt/netbox/netbox/scripts/

mv /opt/netbox/netbox/netbox/configuration_example.py /opt/netbox/netbox/netbox/configuration.py

SECRET_KEY=$( 3 /opt/netbox/netbox/generate_secret_key.py)
ESCAPED_SECRET_KEY=$(printf '%s\n' "$SECRET_KEY" | sed 's/[&/\]/\\&/g')

sed -i 's/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = ["*"]/' /opt/netbox/netbox/netbox/configuration.py
sed -i "s|SECRET_KEY = ''|SECRET_KEY = '${ESCAPED_SECRET_KEY}'|" /opt/netbox/netbox/netbox/configuration.py
sed -i "/DATABASE = {/,/}/s/'USER': '[^']*'/'USER': '$DB_USER'/" /opt/netbox/netbox/netbox/configuration.py
sed -i "/DATABASE = {/,/}/s/'PASSWORD': '[^']*'/'PASSWORD': '$DB_PASS'/" /opt/netbox/netbox/netbox/configuration.py

/opt/netbox/upgrade.sh
ln -s /opt/netbox/contrib/netbox-housekeeping.sh /etc/cron.daily/netbox-housekeeping

mv /opt/netbox/contrib/apache.conf /etc/apache2/sites-available/netbox.conf
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/netbox.key -out /etc/ssl/certs/netbox.crt -subj "/C=US/O=NetBox/OU=Certificate/CN=localhost"
a2enmod ssl proxy proxy_http headers rewrite
a2ensite netbox
systemctl restart apache2

mv /opt/netbox/contrib/gunicorn.py /opt/netbox/gunicorn.py
mv /opt/netbox/contrib/*.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now netbox netbox-rq

echo "${RELEASE}" >/opt/netbox_version.txt
echo -e "Netbox Secret: \e[32m$SECRET_KEY\e[0m" >> ~/netbox.creds
msg_ok "Installed NetBox"

# Set up Django Admin
msg_info "Setting up Django Admin"
DJANGO_USER=Admin
DJANGO_PASS=$(openssl rand -base64 18 | tr -dc 'a-zA-Z0-9' | cut -c1-13)

source /opt/netbox/venv/bin/activate
python3 /opt/netbox/netbox/manage.py shell << EOF
from django.contrib.auth import get_user_model
UserModel = get_user_model()
user = UserModel.objects.create_user('$DJANGO_USER', password='$DJANGO_PASS')
user.is_superuser = True
user.is_staff = True
user.save()
EOF

{
echo ""
echo "Netbox-Django-Credentials"
echo -e "Django User: \e[32m$DJANGO_USER\e[0m"
echo -e "Django Password: \e[32m$DJANGO_PASS\e[0m"
} >> ~/netbox.creds
msg_ok "Setup Django Admin"

# Cleanup
msg_info "Cleaning up"
rm "/opt/v${RELEASE}.zip"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with access details
msg_info "NetBox installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "NetBox is running and accessible at: https://$IP_ADDRESS/"
echo "Django Admin Interface: https://$IP_ADDRESS/admin/"
echo "Database and Admin credentials saved to ~/netbox.creds."
