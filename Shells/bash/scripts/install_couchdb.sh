#!/usr/bin/env  

# Apache CouchDB Installation Script for Ubuntu 22 WSL2 without systemd

# Functions to display messages
msg_info() {
    echo -e "\e[34m[INFO]\e[0m $1"
}

msg_ok() {
    echo -e "\e[32m[OK]\e[0m $1"
}

msg_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
}

# Update the OS
msg_info "Updating OS"
sudo apt-get update && sudo apt-get upgrade -y
msg_ok "OS Updated"

# Install Dependencies
msg_info "Installing Dependencies"
sudo apt-get install -y curl sudo mc apt-transport-https gnupg
msg_ok "Installed Dependencies"

# Install Apache CouchDB
msg_info "Installing Apache CouchDB"

ERLANG_COOKIE=$(openssl rand -base64 32)
ADMIN_PASS="$(openssl rand -base64 18 | cut -c1-13)"

sudo debconf-set-selections <<< "couchdb couchdb/cookie string $ERLANG_COOKIE"
sudo debconf-set-selections <<< "couchdb couchdb/mode select standalone"
sudo debconf-set-selections <<< "couchdb couchdb/bindaddress string 0.0.0.0"
sudo debconf-set-selections <<< "couchdb couchdb/adminpass password $ADMIN_PASS"
sudo debconf-set-selections <<< "couchdb couchdb/adminpass_again password $ADMIN_PASS"

curl -fsSL https://couchdb.apache.org/repo/keys.asc | sudo gpg --dearmor -o /usr/share/keyrings/couchdb-archive-keyring.gpg

VERSION_CODENAME="$(lsb_release -cs)"

echo "deb [signed-by=/usr/share/keyrings/couchdb-archive-keyring.gpg] https://apache.jfrog.io/artifactory/couchdb-deb/ ${VERSION_CODENAME} main" | sudo tee /etc/apt/sources.list.d/couchdb.list

sudo apt-get update
sudo apt-get install -y couchdb

echo -e "CouchDB Erlang Cookie: $ERLANG_COOKIE" >> ~/CouchDB.creds
echo -e "CouchDB Admin Password: $ADMIN_PASS" >> ~/CouchDB.creds

msg_ok "Installed Apache CouchDB."

# Start CouchDB manually
msg_info "Starting CouchDB manually"

# Find the CouchDB executable
COUCHDB_BIN=$(which couchdb || true)

if [ -z "$COUCHDB_BIN" ]; then
    COUCHDB_BIN="/opt/couchdb/bin/couchdb"
    if [ ! -f "$COUCHDB_BIN" ]; then
        msg_error "CouchDB executable not found."
        exit 1
    fi
fi

# Start CouchDB in the background
sudo -u couchdb "$COUCHDB_BIN" -b

msg_ok "CouchDB started manually"

# Clean up
msg_info "Cleaning up"
sudo apt-get -y autoremove
sudo apt-get -y autoclean
msg_ok "Cleaned"
