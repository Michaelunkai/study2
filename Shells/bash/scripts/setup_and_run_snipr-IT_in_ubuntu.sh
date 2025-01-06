#!/usr/bin/env  

# Name: setup_snipeit.sh
# Description: Script to install Snipe-IT on Ubuntu
# Author: Michel Roegl-Brunner
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
    git \
    sudo \
    mc \
    nginx \
    mariadb-server
msg_ok "Dependencies installed"

# Install PHP and Composer
msg_info "Installing PHP and Composer"
apt-get install -y php php-cli php-fpm php-json php-common php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath
curl -sS https://getcomposer.org/installer | php
mv composer.phar /usr/local/bin/composer
composer --version
msg_ok "PHP and Composer installed"

# Set up database
msg_info "Setting up database"
DB_NAME="snipeit_db"
DB_USER="snipeit"
DB_PASS=$(openssl rand -base64 18 | tr -dc 'a-zA-Z0-9' | head -c13)
mysql -u root -e "CREATE DATABASE $DB_NAME;"
mysql -u root -e "CREATE USER '$DB_USER'@'localhost' IDENTIFIED WITH mysql_native_password AS PASSWORD('$DB_PASS');"
mysql -u root -e "GRANT ALL ON $DB_NAME.* TO '$DB_USER'@'localhost'; FLUSH PRIVILEGES;"
{
    echo "SnipeIT-Credentials"
    echo "Database User: $DB_USER"
    echo "Database Password: $DB_PASS"
    echo "Database Name: $DB_NAME"
} > ~/snipeit.creds
msg_ok "Database setup complete"

# Install Snipe-IT
msg_info "Installing Snipe-IT"
cd /opt
RELEASE=$(curl -s https://api.github.com/repos/snipe/snipe-it/releases/latest | grep "tag_name" | awk '{print substr($2, 3, length($2)-4) }')
wget -q "https://github.com/snipe/snipe-it/archive/refs/tags/v${RELEASE}.zip"
unzip -q "v${RELEASE}.zip"
mv "snipe-it-${RELEASE}" /opt/snipe-it

cd /opt/snipe-it
cp .env.example .env
IPADDRESS=$(hostname -I | awk '{print $1}')

sed -i -e "s|^APP_URL=.*|APP_URL=http://$IPADDRESS|" \
       -e "s|^DB_DATABASE=.*|DB_DATABASE=$DB_NAME|" \
       -e "s|^DB_USERNAME=.*|DB_USERNAME=$DB_USER|" \
       -e "s|^DB_PASSWORD=.*|DB_PASSWORD=$DB_PASS|" .env

chown -R www-data: /opt/snipe-it
chmod -R 755 /opt/snipe-it

composer update --no-plugins --no-scripts
composer install --no-dev --prefer-source --no-plugins --no-scripts

php artisan key:generate --force
msg_ok "Snipe-IT installed"

# Configure Nginx
msg_info "Configuring Nginx"
cat <<EOF >/etc/nginx/conf.d/snipeit.conf
server {
    listen 80;
    root /opt/snipe-it/public;
    server_name $IPADDRESS;
    index index. ;

    location / {
        try_files \$uri \$uri/ /index.php?\$query_string;
    }

    location ~ \.php\$ {
        include fastcgi.conf;
        include snippets/fastcgi- .conf;
        fastcgi_pass unix:/run/ / -fpm.sock;
        fastcgi_split_path_info ^(.+\. )(/.+)\$;
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        include fastcgi_params;
    }
}
EOF

systemctl reload nginx
msg_ok "Nginx configured"

# Cleanup
msg_info "Cleaning up"
rm -rf "/opt/v${RELEASE}.zip"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Snipe-IT installation complete"
echo "Snipe-IT is running and accessible at: http://$IPADDRESS"
echo "Database credentials saved in ~/snipeit.creds"
