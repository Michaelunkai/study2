#!/bin/ 

# Update package list and install Java Development Kit
sudo apt-get update
sudo apt-get install -y default-jdk

# Create a dedicated user for ZooKeeper
sudo useradd zookeeper -m -s /bin/bash
echo "zookeeper:your_password" | sudo chpasswd
sudo usermod -aG sudo zookeeper

# Create a data directory for ZooKeeper
sudo mkdir -p /data/zookeeper
sudo chown -R zookeeper:zookeeper /data/zookeeper

# Download and extract ZooKeeper
cd /opt
sudo wget https://archive.apache.org/dist/zookeeper/zookeeper-3.6.1/apache-zookeeper-3.6.1-bin.tar.gz
sudo tar -xvf apache-zookeeper-3.6.1-bin.tar.gz
sudo mv apache-zookeeper-3.6.1-bin zookeeper
sudo chown -R zookeeper:zookeeper /opt/zookeeper

# Configure ZooKeeper
sudo -u zookeeper bash -c 'cat << EOF > /opt/zookeeper/conf/zoo.cfg
tickTime=2000
dataDir=/data/zookeeper
clientPort=2181
initLimit=5
syncLimit=2
EOF'

# Create systemd service file for ZooKeeper
sudo bash -c 'cat << EOF > /etc/systemd/system/zookeeper.service
[Unit]
Description=ZooKeeper Service
After=network.target

[Service]
User=zookeeper
Group=zookeeper
ExecStart=/opt/zookeeper/bin/zkServer.sh start
ExecStop=/opt/zookeeper/bin/zkServer.sh stop
Restart=on-failure
WorkingDirectory=/opt/zookeeper

[Install]
WantedBy=multi-user.target
EOF'

# Reload systemd, enable and start ZooKeeper service
sudo systemctl daemon-reload
sudo systemctl enable zookeeper
sudo systemctl start zookeeper

