#!/bin/ 

# Install OpenJDK 11
sudo apt install openjdk-11-jdk -y

# Download Metabase
cd /opt
sudo wget https://downloads.metabase.com/v0.46.1/metabase.jar

# Create a Metabase user
sudo useradd -r -s /bin/false metabase
sudo chown -R metabase:metabase /opt/metabase.jar

# Create systemd service file
sudo bash -c 'cat > /etc/systemd/system/metabase.service <<EOF
[Unit]
Description=Metabase server
After=syslog.target
After=network.target

[Service]
WorkingDirectory=/opt
ExecStart=/usr/bin/java -jar /opt/metabase.jar
User=metabase
Type=simple
Standard =syslog
StandardError=syslog
SyslogIdentifier=metabase
SuccessExitStatus=143
TimeoutStopSec=120
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

# Reload systemd, start and enable Metabase service
sudo systemctl daemon-reload
sudo systemctl start metabase
sudo systemctl enable metabase

# Check the status of Metabase service
sudo systemctl status metabase

# Open Metabase in Chrome (Windows specific)
cmd.exe /c start chrome http://localhost:3000
