#!/bin/ 

# Update system packages
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install dependencies
echo "Installing dependencies..."
sudo apt install -y ffmpeg libmariadb3 libpq5 libmicrohttpd12

# Install Motion
echo "Installing Motion..."
sudo apt install -y motion

# Stop Motion daemon if it's running
echo "Stopping Motion service if running..."
sudo systemctl stop motion

# Install Python3 and pip
echo "Installing Python3 and pip..."
sudo apt install -y python3 python3-pip python3-dev

# Install MotionEye using pip
echo "Installing MotionEye..."
sudo pip3 install motioneye

# Create configuration directory and copy sample configuration
echo "Configuring MotionEye..."
sudo mkdir -p /etc/motioneye
sudo cp /usr/local/share/motioneye/extra/motioneye.conf.sample /etc/motioneye/motioneye.conf

# Create media directory
sudo mkdir -p /var/lib/motioneye

# Copy systemd service file
echo "Setting up systemd service for MotionEye..."
sudo cp /usr/local/share/motioneye/extra/motioneye.systemd-unit-local /etc/systemd/system/motioneye.service

# Reload systemd services and enable MotionEye service
echo "Enabling and starting MotionEye service..."
sudo systemctl daemon-reload
sudo systemctl enable motioneye
sudo systemctl start motioneye

# Check the status of MotionEye service
sudo systemctl status motioneye

echo "MotionEye installation and setup complete."
echo "You can access the web interface at http://<your_ip_address>:8765/"
