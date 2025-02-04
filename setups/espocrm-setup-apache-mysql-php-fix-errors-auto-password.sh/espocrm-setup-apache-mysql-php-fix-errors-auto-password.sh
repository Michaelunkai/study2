#!/bin/ 

# Update and install required packages
sudo apt update
sudo apt install -y apache2 mysql-server php php-mysql libapache2-mod-php php-curl php-json php-gd php-mbstring php-intl php-xml php-zip php-bcmath php-imap unzip git

# Set MySQL root password to '123456' and configure MySQL non-interactively
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password 123456'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 123456'
sudo apt-get -y install mysql-server

# Clone the EspoCRM repository
git clone https://github.com/espocrm/espocrm.git
cd espocrm

# Set up MySQL database with user and password
sudo mysql -u root -p123456 <<EOF
CREATE DATABASE espocrm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'espocrmuser'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON espocrm.* TO 'espocrmuser'@'localhost';
FLUSH PRIVILEGES;
EOF

# Configure Apache
sudo bash -c 'cat <<EOT > /etc/apache2/sites-available/espocrm.conf
<VirtualHost *:80>
    ServerAdmin admin@localhost
    DocumentRoot /var/www/html/espocrm/public
    ServerName localhost

    Alias /client/ /var/www/html/espocrm/client/

    <Directory /var/www/html/espocrm/public>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOT'

# Enable site and modules
sudo mkdir -p /var/www/html/espocrm
sudo mv * /var/www/html/espocrm/
sudo a2ensite espocrm.conf
sudo a2enmod rewrite
sudo systemctl restart apache2

# Fix missing vendor files by running composer install
cd /var/www/html/espocrm
curl -sS https://getcomposer.org/installer | php
  composer.phar install

# Secure installation
sudo chown -R www-data:www-data /var/www/html/espocrm
sudo chmod -R 755 /var/www/html/espocrm

# Open EspoCRM in Chrome
cmd.exe /c start chrome http://localhost:$1

echo "EspoCRM setup is complete. Access it at http://localhost:$1"
