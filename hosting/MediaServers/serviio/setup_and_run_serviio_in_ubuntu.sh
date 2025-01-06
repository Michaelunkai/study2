#!/bin/ 

# Update system and install required packages
echo "Installing required packages..."
sudo apt update
sudo apt install -y net-tools software-properties-common openjdk-11-jre default-jre ffmpeg dcraw wget

echo "Packages installed successfully."

# Change to installation directory
echo "Switching to /opt directory..."
cd /opt || { echo "Failed to change directory to /opt"; exit 1; }

# Download Serviio
echo "Downloading Serviio..."
sudo wget http://download.serviio.org/releases/serviio-2.4-linux.tar.gz

# Extract Serviio
echo "Extracting Serviio..."
sudo tar zxvf serviio-2.4-linux.tar.gz

# Create a soft link
echo "Creating a symbolic link for Serviio..."
sudo ln -s serviio-2.4 serviio

# Change ownership of the Serviio files
echo "Changing ownership of Serviio files to root..."
sudo chown -R root:root /opt/serviio-2.4

# Remove installation file
echo "Removing installation file..."
sudo rm serviio-2.4-linux.tar.gz

# Create serviio.service file
echo "Creating serviio.service file..."
sudo bash -c 'cat <<EOF > /lib/systemd/system/serviio.service
[Unit]
Description=Serviio Media Server
After=syslog.target local-fs.target network.target

[Service]
Type=simple
Standard =null
ExecStart=/opt/serviio/bin/serviio.sh
ExecStop=/opt/serviio/bin/serviio.sh -stop
KillMode=mixed
TimeoutStopSec=30
Restart=on-abort

[Install]
WantedBy=multi-user.target
EOF'

# Enable and start the Serviio service
echo "Reloading system daemon, enabling and starting Serviio service..."
sudo systemctl daemon-reload
sudo systemctl enable serviio.service
sudo systemctl start serviio.service

# Final message with URL
echo "Serviio installation and setup completed successfully!"
echo "You can access the Serviio console at: http://localhost:23423/console/#/app/welcome"
