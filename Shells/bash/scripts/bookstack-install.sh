#!/usr/bin/env bash

# Copyright (c) 2021-2024 community-scripts ORG
# Author: MickLesk (Canbiz)
# License: MIT
# https://github.com/community-scripts/ProxmoxVE/raw/main/LICENSE

set -e
set -o pipefail

# Helper Functions
msg_info() { echo -e "\e[34m[INFO]\e[0m $1"; }
msg_ok() { echo -e "\e[32m[OK]\e[0m $1"; }
msg_error() { echo -e "\e[31m[ERROR]\e[0m $1"; exit 1; }

# Check for sudo privileges
if [ "$EUID" -ne 0 ]; then
  msg_error "Please run as root"
fi

# Update the OS
msg_info "Updating the OS"
apt-get update && apt-get upgrade -y
msg_ok "Updated the OS"

# Install dependencies
msg_info "Installing Dependencies (Patience)"
apt-get install -y unzip mariadb-server apache2 curl sudo make mc
sudo apt install -y php php-cli php-fpm php-json php-common php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath \
&& curl -sS https://getcomposer.org/installer | php \
&& sudo mv composer.phar /usr/local/bin/composer && composer --version
msg_ok "Installed Dependencies"

# Setup Database
msg_info "Setting up Database"
DB_NAME="bookstack"
DB_USER="bookstack"
DB_PASS=$(openssl rand -base64 18 | tr -dc 'a-zA-Z0-9' | head -c13)
mysql -u root <<EOF
CREATE DATABASE $DB_NAME;
CREATE USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF
cat <<EOF > ~/bookstack.creds
Bookstack-Credentials:
Database User: $DB_USER
Database Password: $DB_PASS
Database Name: $DB_NAME
EOF
msg_ok "Set up database"

# Setup BookStack
msg_info "Setting up BookStack (Patience)"
LOCAL_IP=$(hostname -I | awk '{print $1}')
cd /opt
RELEASE=$(curl -s https://api.github.com/repos/BookStackApp/BookStack/releases/latest | grep "tag_name" | awk '{print substr($2, 3, length($2)-4) }')
wget -q "https://github.com/BookStackApp/BookStack/archive/refs/tags/v${RELEASE}.zip"
unzip -q v${RELEASE}.zip
mv BookStack-${RELEASE} /opt/bookstack
cd /opt/bookstack
cp .env.example .env
sed -i "s|APP_URL=.*|APP_URL=http://$LOCAL_IP|g" .env
sed -i "s/DB_DATABASE=.*/DB_DATABASE=$DB_NAME/" .env
sed -i "s/DB_USERNAME=.*/DB_USERNAME=$DB_USER/" .env
sed -i "s/DB_PASSWORD=.*/DB_PASSWORD=$DB_PASS/" .env
composer install --no-dev --no-interaction
php artisan key:generate --no-interaction
php artisan migrate --no-interaction
chown -R www-data:www-data /opt/bookstack
chmod -R 775 /opt/bookstack/storage /opt/bookstack/bootstrap/cache
chmod -R 640 /opt/bookstack/.env
msg_ok "Setup BookStack"

# Configure Apache
msg_info "Configuring Apache"
cat <<EOF > /etc/apache2/sites-available/bookstack.conf
<VirtualHost *:80>
  ServerAdmin webmaster@localhost
  DocumentRoot /opt/bookstack/public/

  <Directory /opt/bookstack/public/>
      Options -Indexes +FollowSymLinks
      AllowOverride None
      Require all granted

      RewriteEngine On
      RewriteCond %{REQUEST_FILENAME} !-d
      RewriteCond %{REQUEST_FILENAME} !-f
      RewriteRule ^ index.php [L]
  </Directory>

  ErrorLog \${APACHE_LOG_DIR}/error.log
  CustomLog \${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF
a2enmod rewrite php8.2
a2ensite bookstack
a2dissite 000-default
systemctl reload apache2
msg_ok "Configured Apache"

# Clean up
msg_info "Cleaning up"
rm -rf /opt/v${RELEASE}.zip
apt-get autoremove -y
apt-get autoclean -y
msg_ok "Cleaned up"

# Display URL for Web UI
msg_ok "Installation complete. Access BookStack at: http://$LOCAL_IP"
