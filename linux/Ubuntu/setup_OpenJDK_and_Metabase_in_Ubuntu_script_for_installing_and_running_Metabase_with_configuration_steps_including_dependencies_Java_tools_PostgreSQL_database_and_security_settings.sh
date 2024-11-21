#!/bin/ 

# Update package list and install OpenJDK 11
sudo apt update
sudo apt install -y openjdk-11-jdk

# Verify Java installation
java -version

# Add Metabase user
sudo useradd -r -m -U -d /opt/metabase -s /bin/bash metabase

# Download and set up Metabase
cd /opt/metabase
sudo wget https://downloads.metabase.com/v0.45.2/metabase.jar
sudo chown metabase:metabase /opt/metabase/metabase.jar

# Set up Metabase service
sudo bash -c 'cat << EOF > /etc/systemd/system/metabase.service
[Unit]
Description=Metabase Server
After=syslog.target
After=network.target

[Service]
WorkingDirectory=/opt/metabase
ExecStart=/usr/bin/java -jar /opt/metabase/metabase.jar
User=metabase
Type=simple
Restart=always
RestartSec=10
Standard =syslog
StandardError=syslog
SyslogIdentifier=metabase

[Install]
WantedBy=multi-user.target
EOF'

# Reload systemd and start Metabase
sudo systemctl daemon-reload
sudo systemctl start metabase
sudo systemctl enable metabase

# Verify Metabase status
sudo systemctl status metabase

# Install PostgreSQL (optional, replace with your desired DB setup)
sudo apt install -y postgresql postgresql-contrib

# Create a PostgreSQL user and database for Metabase
sudo -u postgres createuser metabase_user
sudo -u postgres createdb metabase_db -O metabase_user

# Set PostgreSQL password for the user
sudo -u postgres psql -c "ALTER USER metabase_user WITH PASSWORD 'yourpassword';"

# Edit PostgreSQL config to allow external connections (if needed)
sudo bash -c 'echo "listen_addresses = '*'" >> /etc/postgresql/12/main/postgresql.conf'
sudo bash -c 'echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/12/main/pg_hba.conf'

# Restart PostgreSQL
sudo systemctl restart postgresql

# End of script
echo "OpenJDK and Metabase installation complete. Access Metabase at http://your_server_ip:3000"
