#!/usr/bin/env bash

# Update package lists
sudo apt-get update

# Install dependencies
sudo apt-get install -y curl git make g++ gcc openssh-server nano mc

# Install Node.js LTS (version 18.x)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Clone Zigbee2MQTT repository
sudo git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt

# Install Zigbee2MQTT dependencies
cd /opt/zigbee2mqtt
sudo npm ci

# Create configuration file if it doesn't exist
sudo cp -n data/configuration.example.yaml data/configuration.yaml

# Modify permissions
sudo chown -R $USER:$USER /opt/zigbee2mqtt

# Enable the frontend in configuration.yaml
if ! grep -q "frontend:" data/configuration.yaml; then
    echo "frontend:" >> data/configuration.yaml
    echo "  port: 8080" >> data/configuration.yaml
    echo "  host: 0.0.0.0" >> data/configuration.yaml
fi

# Create systemd service file
sudo tee /etc/systemd/system/zigbee2mqtt.service > /dev/null <<EOF
[Unit]
Description=Zigbee2MQTT
After=network.target

[Service]
ExecStart=/usr/bin/npm start
WorkingDirectory=/opt/zigbee2mqtt
StandardOutput=inherit
StandardError=inherit
Restart=always
User=$USER
Environment="PATH=/usr/bin:/usr/local/bin"
Environment="NODE_ENV=production"

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable and start zigbee2mqtt service
sudo systemctl enable zigbee2mqtt
sudo systemctl start zigbee2mqtt

# Display status
sudo systemctl status zigbee2mqtt

# Echo the WebUI URL
IP_ADDRESS=$(hostname -I | awk '{print $1}')
PORT=$(grep "port:" data/configuration.yaml | awk '{print $2}')
echo "Zigbee2MQTT WebUI is available at: http://$IP_ADDRESS:$PORT"
