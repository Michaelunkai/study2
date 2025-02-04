#!/usr/bin/env  

# Name: setup_wavelog.sh
# Description: Script to install Wavelog on Ubuntu
# Author: Don Locke (DonLocke)
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
    libapache2-mod-  \
    mariadb-server \
    mc \
     8.2-{curl,mbstring,my ,xml,zip,gd} \
    sudo \
    unzip
msg_ok "Dependencies installed"

# Set up the database
msg_info "Setting up Database"
DB_NAME=wavelog
DB_USER=waveloguser
DB_PASS=$(openssl rand -base64 18 | tr -dc 'a-zA-Z0-9' | head -c13)
mysql -u root -e "CREATE DATABASE $DB_NAME;"
mysql -u root -e "CREATE USER '$DB_USER'@'localhost' IDENTIFIED WITH mysql_native_password AS PASSWORD('$DB_PASS');"
mysql -u root -e "GRANT ALL ON $DB_NAME.* TO '$DB_USER'@'localhost'; FLUSH PRIVILEGES;"

cat <<EOF > ~/wavelog.creds
Wavelog-Credentials
Wavelog Database User: $DB_USER
Wavelog Database Password: $DB_PASS
Wavelog Database Name: $DB_NAME
EOF
msg_ok "Database configured"

# Set up PHP
msg_info "Setting up PHP"
sed -i '/max_execution_time/s/= .*/= 600/' /etc/php/8.2/apache2/php.ini
sed -i '/memory_limit/s/= .*/= 256M/' /etc/php/8.2/apache2/php.ini
sed -i '/upload_max_filesize/s/= .*/= 8M/' /etc/php/8.2/apache2/php.ini
msg_ok "PHP configured"

# Install Wavelog
msg_info "Installing Wavelog"
RELEASE=$(curl -s https://api.github.com/repos/wavelog/wavelog/releases/latest | grep "tag_name" | awk '{print substr($2, 2, length($2)-3) }')
wget -q "https://github.com/wavelog/wavelog/archive/refs/tags/${RELEASE}.zip"
unzip -q ${RELEASE}.zip
mv wavelog-${RELEASE}/ /opt/wavelog
chown -R www-data:www-data /opt/wavelog/
find /opt/wavelog/ -type d -exec chmod 755 {} \;
find /opt/wavelog/ -type f -exec chmod 664 {} \;
echo "${RELEASE}" >/opt/wavelog_version.txt
msg_ok "Wavelog installed"

# Configure Apache service
msg_info "Creating Service"
cat <<EOF >/etc/apache2/sites-available/wavelog.conf
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /opt/wavelog

    <Directory /opt/wavelog>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog /var/log/apache2/error.log
    CustomLog /var/log/apache2/access.log combined
</VirtualHost>
EOF

a2ensite wavelog.conf
a2dissite 000-default.conf
systemctl reload apache2
msg_ok "Apache service configured"

# Cleanup
msg_info "Cleaning up"
rm -f ${RELEASE}.zip
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Wavelog installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Wavelog is running and accessible at: http://$IP_ADDRESS"
echo ""
echo "### Wavelog: Blogging Platform"
echo "A user-friendly and customizable blogging platform for creating and managing content."
