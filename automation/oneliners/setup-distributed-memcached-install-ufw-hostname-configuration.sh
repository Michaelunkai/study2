#!/bin/ 

# Script Name: setup-distributed-memcached.sh
# Description: Automates the setup of a distributed Memcached cluster on Ubuntu servers.

# Exit immediately if a command exits with a non-zero status
set -e

# Define Variables
APPLICATION_SERVER_IP="192.168.1.20"  # IP of the application server
MEMCACHED_PORT="11211"                # Default Memcached port
MEMCACHED_MEMORY="512"                # Memory allocation in MB
MEMCACHED_CONNECTIONS="1024"          # Maximum simultaneous connections

# Determine the server's private IP address
PRIVATE_IP=$(hostname -I | awk '{print $1}')

# Set Hostname based on private IP
HOSTNAME="memcached-$(echo $PRIVATE_IP | awk -F. '{print $4}')"
echo "Setting hostname to $HOSTNAME"
hostnamectl set-hostname $HOSTNAME

# Install Memcached and libmemcached-tools
echo "Installing Memcached and dependencies..."
sudo apt-get install memcached libmemcached-tools -y

# Backup existing Memcached configuration
sudo cp /etc/memcached.conf /etc/memcached.conf.bak

# Configure Memcached
echo "Configuring Memcached..."
sudo bash -c "cat > /etc/memcached.conf" <<EOL
# Memcached Configuration File

# Listen on the server's private IP
-l $PRIVATE_IP

# Memory usage in MB
-m $MEMCACHED_MEMORY

# Port to listen on
-p $MEMCACHED_PORT

# Maximum simultaneous connections
-c $MEMCACHED_CONNECTIONS

# Disable UDP support for security
-u memcache
-D

# Verbosity level (0 = no verbosity)
-v 0
EOL

# Restart Memcached to apply changes
echo "Restarting Memcached service..."
sudo systemctl restart memcached

# Enable Memcached to start on boot
sudo systemctl enable memcached

# Configure UFW Firewall
echo "Configuring UFW firewall rules..."

# Check if UFW is active
if sudo ufw status | grep -q "Status: inactive"; then
    echo "Enabling UFW..."
    sudo ufw enable
fi

# Allow SSH connections
sudo ufw allow ssh

# Allow Memcached port from the application server
sudo ufw allow from $APPLICATION_SERVER_IP to any port $MEMCACHED_PORT

# Deny all other incoming connections to Memcached port
sudo ufw deny $MEMCACHED_PORT

# Reload UFW to apply changes
sudo ufw reload

# Display Memcached status
echo "Memcached service status:"
sudo systemctl status memcached --no-pager

# Display UFW status
echo "UFW firewall status:"
sudo ufw status

echo "Distributed Memcached setup completed successfully on $HOSTNAME."
