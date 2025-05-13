#!/usr/bin/env  

# Name: setup_pialert.sh
# Description: Script to install Pi.Alert on Ubuntu
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

# Install required dependencies
msg_info "Installing Dependencies"
apt-get update && apt-get install -y \
    sudo \
    mc \
    curl \
    apt-utils \
    avahi-utils \
    lighttpd \
     ite3 \
    mmdb-bin \
    arp-scan \
    dnsutils \
    net-tools \
    nbtscan \
    libwww-perl \
    nmap \
    zip \
    aria2 \
    wakeonlan
msg_ok "Installed Dependencies"

# Install PHP dependencies
msg_info "Installing PHP Dependencies"
apt-get install -y \
      \
     -cgi \
     -fpm \
     -curl \
     -xml \
     - ite3
lighttpd-enable-mod fastcgi- 
service lighttpd force-reload
msg_ok "Installed PHP Dependencies"

# Install Python dependencies
msg_info "Installing Python Dependencies"
apt-get install -y \
     3-pip \
     3-requests \
     3-tz \
     3-tzlocal
rm -rf /usr/lib/ 3.*/EXTERNALLY-MANAGED
pip3 install mac-vendor-lookup fritzconnection cryptography pyunifi
msg_ok "Installed Python Dependencies"

# Install Pi.Alert
msg_info "Installing Pi.Alert"
curl -sL https://github.com/leiweibau/Pi.Alert/raw/main/tar/pialert_latest.tar | tar xvf - -C /opt >/dev/null 2>&1
rm -rf /var/lib/ieee-data /var/www/html/index.html
sed -i -e 's#^sudo cp -n /usr/share/ieee-data/.* /var/lib/ieee-data/#\# &#' -e '/^sudo mkdir -p 2_backup$/s/^/# /' -e '/^sudo cp \*.txt 2_backup$/s/^/# /' -e '/^sudo cp \*.csv 2_backup$/s/^/# /' /opt/pialert/back/update_vendors.sh
mv /var/www/html/index.lighttpd.html /var/www/html/index.lighttpd.html.old
ln -s /usr/share/ieee-data/ /var/lib/
ln -s /opt/pialert/install/index.html /var/www/html/index.html
ln -s /opt/pialert/front /var/www/html/pialert
chmod go+x /opt/pialert /opt/pialert/back/shoutrrr/x86/shoutrrr
chgrp -R www-data /opt/pialert/db /opt/pialert/front/reports /opt/pialert/config /opt/pialert/config/pialert.conf
chmod -R 775 /opt/pialert/db /opt/pialert/db/temp /opt/pialert/config /opt/pialert/front/reports
touch /opt/pialert/log/{pialert.vendors.log,pialert.IP.log,pialert.1.log,pialert.cleanup.log,pialert.webservices.log}
src_dir="/opt/pialert/log"
dest_dir="/opt/pialert/front/ /server"
for file in pialert.vendors.log pialert.IP.log pialert.1.log pialert.cleanup.log pialert.webservices.log; do
    ln -s "$src_dir/$file" "$dest_dir/$file"
done
sed -i 's#PIALERT_PATH\s*=\s*'\''/home/pi/pialert'\''#PIALERT_PATH           = '\''/opt/pialert'\''#' /opt/pialert/config/pialert.conf
sed -i 's/$HOME/\/opt/g' /opt/pialert/install/pialert.cron
crontab /opt/pialert/install/pialert.cron
echo "python3 /opt/pialert/back/pialert.py 1" >/usr/bin/scan
chmod +x /usr/bin/scan
echo "/opt/pialert/back/pialert-cli set_permissions --lxc" >/usr/bin/permissions
chmod +x /usr/bin/permissions
echo "/opt/pialert/back/pialert-cli set_sudoers --lxc" >/usr/bin/sudoers
chmod +x /usr/bin/sudoers
msg_ok "Installed Pi.Alert"

# Start Pi.Alert scan
msg_info "Start Pi.Alert Scan (Patience)"
 3 /opt/pialert/back/pialert.py update_vendors
 3 /opt/pialert/back/pialert.py internet_IP
 3 /opt/pialert/back/pialert.py 1
msg_ok "Finished Pi.Alert Scan"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL
msg_info "Pi.Alert installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Pi.Alert is running and accessible at: http://$IP_ADDRESS/pialert"
