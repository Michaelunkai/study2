#!/bin/ 

# Check if run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Variables
CACTI_DB_PASSWORD='YourStrongPasswordHere'  # Replace with a strong password

# Update system packages
apt update -y
apt upgrade -y

# Install dependencies
apt-get install snmp php-snmp rrdtool librrds-perl unzip git gnupg2 -y

# Install Apache, PHP, MariaDB, and extensions
apt-get install apache2 mariadb-server php php-mysql php-intl libapache2-mod-php php-xml php-ldap php-mbstring php-gd php-gmp -y

# Enable PHP MySQL module
PHP_VER=$(php -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')
 enmod my i
 enmod my 
systemctl restart apache2

# Modify php.ini files
sed -i "s/^memory_limit = .*/memory_limit = 512M/" /etc/php/$PHP_VER/apache2/php.ini
sed -i "s/^max_execution_time = .*/max_execution_time = 360/" /etc/php/$PHP_VER/apache2/php.ini
sed -i "s|^;date.timezone =.*|date.timezone = UTC|" /etc/php/$PHP_VER/apache2/php.ini

sed -i "s/^memory_limit = .*/memory_limit = 512M/" /etc/php/$PHP_VER/cli/php.ini
sed -i "s/^max_execution_time = .*/max_execution_time = 360/" /etc/php/$PHP_VER/cli/php.ini
sed -i "s|^;date.timezone =.*|date.timezone = UTC|" /etc/php/$PHP_VER/cli/php.ini

# Restart Apache
systemctl restart apache2

# Start and enable MariaDB
systemctl start mariadb
systemctl enable mariadb

# Secure MariaDB installation (optional, you can automate this if needed)
my _secure_installation <<EOF

y
YourRootDBPasswordHere
YourRootDBPasswordHere
y
y
y
y
EOF

# Create database and user for Cacti
mysql -u root -pYourRootDBPasswordHere -e "CREATE DATABASE cacti CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -pYourRootDBPasswordHere -e "GRANT ALL ON cacti.* TO 'cacti'@'localhost' IDENTIFIED BY '${CACTI_DB_PASSWORD}';"
mysql -u root -pYourRootDBPasswordHere -e "GRANT SELECT ON mysql.time_zone_name TO 'cacti'@'localhost';"
mysql -u root -pYourRootDBPasswordHere -e "FLUSH PRIVILEGES;"

# Import timezone data
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -pYourRootDBPasswordHere mysql

# Adjust MariaDB configuration for Cacti
cat > /etc/mysql/mariadb.conf.d/99-cacti.cnf <<EOL
[my d]
collation-server = utf8mb4_unicode_ci
max_heap_table_size = 128M
tmp_table_size = 64M
join_buffer_size = 64M
innodb_file_format = Barracuda
innodb_large_prefix = 1
innodb_buffer_pool_size = 1024M
innodb_flush_log_at_timeout = 3
innodb_read_io_threads = 32
innodb_write_io_threads = 16
innodb_io_capacity = 5000
innodb_io_capacity_max = 10000
sort_buffer_size = 10M
innodb_doublewrite = OFF
EOL

# Restart MariaDB
systemctl restart mariadb

# Download and install Cacti
wget https://www.cacti.net/downloads/cacti-latest.tar.gz -O cacti-latest.tar.gz
tar -zxvf cacti-latest.tar.gz
mv cacti-*/ /var/www/html/cacti
chown -R www-data:www-data /var/www/html/cacti/

# Import Cacti data to database
mysql -u cacti -p${CACTI_DB_PASSWORD} cacti < /var/www/html/cacti/cacti.sql

# Configure Cacti
cat > /var/www/html/cacti/include/config.php <<EOL
<? 
\$database_type = 'my ';
\$database_default = 'cacti';
\$database_hostname = 'localhost';
\$database_username = 'cacti';
\$database_password = '${CACTI_DB_PASSWORD}';
\$database_port = '3306';
\$database_ssl = false;
?>
EOL

# Create Cron job for Cacti
echo '*/5 * * * * www-data php /var/www/html/cacti/poller.php > /dev/null 2>&1' > /etc/cron.d/cacti

# Create log file for Cacti
mkdir -p /var/www/html/cacti/log/
touch /var/www/html/cacti/log/cacti.log
chown -R www-data:www-data /var/www/html/cacti/

# Create Apache Virtual Host for Cacti
cat > /etc/apache2/sites-available/cacti.conf <<EOL
Alias /cacti /var/www/html/cacti
<Directory /var/www/html/cacti>
    Options +FollowSymLinks
    AllowOverride None
    <IfVersion >= 2.3>
        Require all granted
    </IfVersion>
    <IfVersion < 2.3>
        Order Allow,Deny
        Allow from all
    </IfVersion>
    <IfModule mod_ .c>
         _flag magic_quotes_gpc Off
         _flag short_open_tag On
         _flag register_globals Off
         _flag register_argc_argv On
         _flag track_vars On
         _value mbstring.func_overload 0
         _value include_path .
    </IfModule>
    DirectoryIndex index. 
</Directory>
EOL

# Enable Cacti site and required Apache modules
a2ensite cacti
a2enmod  ${PHP_VER}
a2enmod rewrite
systemctl restart apache2

# Echo URL
echo "Cacti installation is complete. Access it at http://localhost/cacti"
