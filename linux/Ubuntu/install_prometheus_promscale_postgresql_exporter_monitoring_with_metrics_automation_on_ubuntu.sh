#!/bin/ 

# Install Prometheus, Promscale, and PostgreSQL monitoring tools on Ubuntu

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Install essential tools
apt install -y wget tar curl software-properties-common

# Install PostgreSQL
apt install -y postgresql postgresql-contrib

# Start and enable PostgreSQL service
systemctl start postgre 
systemctl enable postgre 

# Set PostgreSQL 'postgres' user password
read -s -p "Enter password for PostgreSQL 'postgres' user: " POSTGRES_PASSWORD
echo
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$POSTGRES_PASSWORD';"

# Create a dedicated database and user for Promscale
read -s -p "Enter password for 'promscale_user': " PROMSCALE_USER_PASSWORD
echo
sudo -u postgres createuser promscale_user --createdb
sudo -u postgres psql -c "ALTER USER promscale_user WITH PASSWORD '$PROMSCALE_USER_PASSWORD';"
sudo -u postgres createdb -O promscale_user promscale_db

# Install Promscale
PROMSCALE_VERSION="0.10.0"
wget https://github.com/timescale/promscale/releases/download/v${PROMSCALE_VERSION}/promscale_${PROMSCALE_VERSION}_linux_amd64.tar.gz
tar -xzf promscale_${PROMSCALE_VERSION}_linux_amd64.tar.gz
mv promscale /usr/local/bin/
rm promscale_${PROMSCALE_VERSION}_linux_amd64.tar.gz

# Create Promscale configuration directory
mkdir -p /etc/promscale

# Create Promscale configuration file
cat <<EOF > /etc/promscale/promscale.yaml
db:
  connection_string: "postgres://promscale_user:${PROMSCALE_USER_PASSWORD}@localhost/promscale_db?sslmode=disable"

listen:
  host: "0.0.0.0"
  port: 9201

prometheus:
  remote_write:
    enabled: true
EOF

# Initialize Promscale schema
promscale --config.file=/etc/promscale/promscale.  migrate

# Create systemd service file for Promscale
cat <<EOF > /etc/systemd/system/promscale.service
[Unit]
Description=Promscale Service
After=network.target

[Service]
User=postgres
ExecStart=/usr/local/bin/promscale --config.file=/etc/promscale/promscale. 
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start Promscale
systemctl daemon-reload
systemctl start promscale
systemctl enable promscale

# Create Prometheus user and directories
useradd --no-create-home --shell /bin/false prometheus
mkdir /etc/prometheus
mkdir /var/lib/prometheus

# Set permissions
chown prometheus:prometheus /etc/prometheus
chown prometheus:prometheus /var/lib/prometheus

# Install Prometheus
PROMETHEUS_VERSION="2.45.0"
wget https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz
tar -xzf prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz
cp prometheus-${PROMETHEUS_VERSION}.linux-amd64/prometheus /usr/local/bin/
cp prometheus-${PROMETHEUS_VERSION}.linux-amd64/promtool /usr/local/bin/
chown prometheus:prometheus /usr/local/bin/prometheus
chown prometheus:prometheus /usr/local/bin/promtool

# Copy console files and set permissions
cp -r prometheus-${PROMETHEUS_VERSION}.linux-amd64/consoles /etc/prometheus/
cp -r prometheus-${PROMETHEUS_VERSION}.linux-amd64/console_libraries /etc/prometheus/
chown -R prometheus:prometheus /etc/prometheus/consoles
chown -R prometheus:prometheus /etc/prometheus/console_libraries

# Create Prometheus configuration file
cat <<EOF > /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

remote_write:
  - url: "http://localhost:9201/write"
EOF

# Set permissions for Prometheus configuration
chown prometheus:prometheus /etc/prometheus/prometheus.yml

# Create systemd service file for Prometheus
cat <<EOF > /etc/systemd/system/prometheus.service
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
ExecStart=/usr/local/bin/prometheus \\
  --config.file=/etc/prometheus/prometheus.yml \\
  --storage.tsdb.path=/var/lib/prometheus/ \\
  --web.console.templates=/etc/prometheus/consoles \\
  --web.console.libraries=/etc/prometheus/console_libraries

Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start Prometheus
systemctl daemon-reload
systemctl start prometheus
systemctl enable prometheus

# Install PostgreSQL Exporter (Optional for SQL Metrics)
read -p "Do you want to install PostgreSQL Exporter for SQL metrics? (y/n): " INSTALL_PG_EXPORTER
if [ "$INSTALL_PG_EXPORTER" == "y" ]; then
  # Download PostgreSQL Exporter
  POSTGRES_EXPORTER_VERSION="0.14.0"
  wget https://github.com/prometheus-community/postgres_exporter/releases/download/v${POSTGRES_EXPORTER_VERSION}/postgres_exporter-${POSTGRES_EXPORTER_VERSION}.linux-amd64.tar.gz
  tar -xzf postgres_exporter-${POSTGRES_EXPORTER_VERSION}.linux-amd64.tar.gz
  mv postgres_exporter-${POSTGRES_EXPORTER_VERSION}.linux-amd64/postgres_exporter /usr/local/bin/
  chown prometheus:prometheus /usr/local/bin/postgres_exporter

  # Create postgres_exporter user and directory
  useradd --no-create-home --shell /bin/false postgres_exporter
  mkdir /etc/postgres_exporter
  chown postgres_exporter:postgres_exporter /etc/postgres_exporter

  # Create .pgpass file for authentication
  cat <<EOF > /etc/postgres_exporter/.pgpass
localhost:5432:promscale_db:promscale_user:${PROMSCALE_USER_PASSWORD}
EOF
  chmod 600 /etc/postgres_exporter/.pgpass
  chown postgres_exporter:postgres_exporter /etc/postgres_exporter/.pgpass

  # Create systemd service file for PostgreSQL Exporter
  cat <<EOF > /etc/systemd/system/postgres_exporter.service
[Unit]
Description=PostgreSQL Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=postgres_exporter
Environment="DATA_SOURCE_NAME=postgre ://promscale_user:${PROMSCALE_USER_PASSWORD}@localhost/promscale_db?sslmode=disable"
ExecStart=/usr/local/bin/postgres_exporter \\
  --web.listen-address=":9187" \\
  --web.telemetry-path="/metrics"

Restart=always

[Install]
WantedBy=multi-user.target
EOF

  # Reload systemd and start PostgreSQL Exporter
  systemctl daemon-reload
  systemctl start postgres_exporter
  systemctl enable postgres_exporter

  # Add PostgreSQL Exporter to Prometheus scrape config
  sed -i '/- job_name: .prometheus./a \ \n  - job_name: '\''postgres_exporter'\''\n    static_configs:\n      - targets: ['\''localhost:9187'\'']' /etc/prometheus/prometheus.yml

  # Reload Prometheus
  systemctl restart prometheus
fi

echo "Setup complete. Prometheus, Promscale, and PostgreSQL are configured and running."
