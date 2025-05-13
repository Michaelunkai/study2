#!/bin/ 

# Download Prometheus
cd && wget https://github.com/prometheus/prometheus/releases/download/v2.37.0/prometheus-2.37.0.linux-amd64.tar.gz

# Extract the tarball
tar -xvf prometheus-2.37.0.linux-amd64.tar.gz

# Move to /etc/prometheus
sudo mv prometheus-2.37.0.linux-amd64 /etc/prometheus

# Create systemd service file
sudo tee /etc/systemd/system/prometheus.service > /dev/null << EOF
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=root
ExecStart=/etc/prometheus/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/var/lib/prometheus --web.console.templates=/etc/prometheus/consoles --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=default.target
EOF

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable and start Prometheus service
sudo systemctl enable prometheus
sudo systemctl start prometheus


# Open Prometheus in the browser
cmd.exe /c start chrome http://localhost:9090
