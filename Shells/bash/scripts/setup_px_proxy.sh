#!/bin/ 

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install dependencies
echo "Installing dependencies..."
sudo apt-get install -y curl wget

# Download and install px proxy (assuming px is available from a remote server)
echo "Downloading and installing px proxy..."
wget https://example.com/path/to/px_proxy_installer.deb -O px_proxy_installer.deb
sudo dpkg -i px_proxy_installer.deb
sudo apt-get -f install -y  # Fix any missing dependencies

# Configure px proxy
echo "Configuring px proxy..."
echo "export http_proxy=http://localhost:3128" >> ~/.bashrc
echo "export https_proxy=http://localhost:3128" >> ~/.bashrc
source ~/. rc

# Start px proxy service
echo "Starting px proxy service..."
sudo systemctl start px_proxy
sudo systemctl enable px_proxy

# Verify px proxy is running
echo "Verifying px proxy service..."
sudo systemctl status px_proxy

echo "Px proxy setup complete!"
