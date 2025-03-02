#!/usr/bin/env  

# Name: setup_shinobi.sh
# Description: Script to install Shinobi CCTV on Ubuntu
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
msg_info "Installing dependencies"
apt-get update && apt-get install -y \
    curl \
    sudo \
    git \
    mc \
    make \
    zip \
    net-tools \
    gcc \
    g++ \
    cmake \
    ca-certificates \
    gnupg
msg_ok "Dependencies installed"

# Set up Node.js repository and install Node.js
msg_info "Setting up Node.js repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
msg_ok "Node.js repository set up"

msg_info "Installing Node.js"
apt-get update && apt-get install -y nodejs
msg_ok "Node.js installed"

# Install FFmpeg
msg_info "Installing FFmpeg"
apt-get install -y ffmpeg
msg_ok "FFmpeg installed"

# Clone Shinobi
msg_info "Cloning Shinobi repository"
cd /opt
git clone https://gitlab.com/Shinobi-Systems/Shinobi.git -b master Shinobi
cd Shinobi
gitVersionNumber=$(git rev-parse HEAD)
theDateRightNow=$(date)
echo '{"Product" : "Shinobi", "Branch" : "master", "Version" : "'"$gitVersionNumber"'", "Date" : "'"$theDateRightNow"'", "Repository" : "https://gitlab.com/Shinobi-Systems/Shinobi.git"}' >version.json
chmod 777 version.json
msg_ok "Shinobi cloned"

# Install MariaDB and configure database
msg_info "Installing and configuring MariaDB"
 user="root"
 pass="root"
echo "mariadb-server mariadb-server/root_password password $sqlpass" | debconf-set-selections
echo "mariadb-server mariadb-server/root_password_again password $sqlpass" | debconf-set-selections
apt-get install -y mariadb-server
service my  start
mysql -u "$sqluser" -p"$sqlpass" -e "source sql/user.sql" || true
msg_ok "MariaDB installed and configured"

# Install Shinobi
msg_info "Installing Shinobi"
cp conf.sample.json conf.json
cronKey=$(head -c 1024 < /dev/urandom | sha256sum | awk '{print substr($1,1,29)}')
sed -i -e 's/Shinobi/'"$cronKey"'/g' conf.json
cp super.sample.json super.json
npm install -g npm
npm install --unsafe-perm
npm install pm2@latest -g
chmod -R 755 .
touch INSTALL/installed.txt
ln -s /opt/Shinobi/INSTALL/shinobi /usr/bin/shinobi
node /opt/Shinobi/tools/modifyConfiguration.js addToConfig="{\"cron\":{\"key\":\"$(head -c 64 < /dev/urandom | sha256sum | awk '{print substr($1,1,60)}')\"}}" &>/dev/null
pm2 start camera.js
pm2 start cron.js
pm2 startup
pm2 save
pm2 list
msg_ok "Shinobi installed"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message
msg_info "Shinobi installation complete"
echo "Shinobi CCTV is running. Access it through your server's IP address."
