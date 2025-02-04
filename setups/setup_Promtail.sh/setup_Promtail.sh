#!/bin/ 

# Variables
PROMTAIL_VERSION="2.10.0"
PROMTAIL_BINARY="promtail-linux-amd64"
PROMTAIL_ZIP="${PROMTAIL_BINARY}.zip"
PROMTAIL_URL="https://github.com/grafana/loki/releases/download/v${PROMTAIL_VERSION}/${PROMTAIL_ZIP}"
PROMTAIL_DEST="/usr/local/bin/promtail"
CONFIG_FILE="/etc/promtail-config. "
SERVICE_FILE="/etc/systemd/system/promtail.service"
LOKI_URL="http://localhost:3100/loki/api/v1/push"  # Adjust this URL as per your Loki server.

# Download Promtail binary
echo "Downloading Promtail..."
wget -q "${PROMTAIL_URL}" -O "${PROMTAIL_ZIP}"

# Unzip and make executable
echo "Unzipping Promtail..."
unzip -q "${PROMTAIL_ZIP}"
chmod +x "${PROMTAIL_BINARY}"

# Move the binary to /usr/local/bin
echo "Moving Promtail to /usr/local/bin..."
sudo mv "${PROMTAIL_BINARY}" "${PROMTAIL_DEST}"

# Create Promtail configuration file
echo "Creating Promtail configuration file..."
sudo bash -c "cat > ${CONFIG_FILE}" <<EOF
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions. 

clients:
  - url: "${LOKI_URL}"

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*log
EOF

# Create a systemd service file for Promtail
echo "Creating Promtail systemd service..."
sudo bash -c "cat > ${SERVICE_FILE}" <<EOF
[Unit]
Description=Promtail service
After=network.target

[Service]
Type=simple
ExecStart=${PROMTAIL_DEST} -config.file=${CONFIG_FILE}
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start Promtail service
echo "Reloading systemd and starting Promtail service..."
sudo systemctl daemon-reload
sudo systemctl enable promtail
sudo systemctl start promtail

# Clean up downloaded files
echo "Cleaning up..."
rm -f "${PROMTAIL_ZIP}"

# Output the Promtail server URL
PROMTAIL_SERVER_URL="http://$(hostname -I | awk '{print $1}'):9080"
echo "Promtail setup complete."
echo "Promtail server is running at: ${PROMTAIL_SERVER_URL}"
