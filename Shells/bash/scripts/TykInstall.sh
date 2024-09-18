#!/bin/ 

# Step 0: Change directory to home
cd

# Step 1: Install dependencies and setup MongoDB and Redis
sudo apt install gnupg curl -y && \
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor && \
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list && \
sudo apt-get update && \
sudo apt-get install -y mongodb-org && \
sudo systemctl start mongod && \
sudo systemctl daemon-reload && \
sudo systemctl enable mongod && \
sudo apt install -y redis-server && \
sudo systemctl start redis-server && \
sudo systemctl enable redis-server

# Variables (replace with your actual values)
UBUNTU_CODENAME="bionic"
REDIS_HOST="<hostname>"
MONGO_IP="<IP Address>"
DOMAIN="<domain>"

# Step 2: Set up our APT Repositories for Tyk Dashboard
curl -L https://packagecloud.io/tyk/tyk-dashboard/gpgkey | sudo apt-key add - && \
sudo apt-get update && \
sudo apt-get install -y apt-transport-https && \
echo "deb https://packagecloud.io/tyk/tyk-dashboard/ubuntu/ $UBUNTU_CODENAME main" | sudo tee /etc/apt/sources.list.d/tyk_tyk-dashboard.list && \
echo "deb-src https://packagecloud.io/tyk/tyk-dashboard/ubuntu/ $UBUNTU_CODENAME main" | sudo tee -a /etc/apt/sources.list.d/tyk_tyk-dashboard.list && \
sudo apt-get update && \
sudo apt-get install -y tyk-dashboard && \
wget https://keyserver.tyk.io/tyk.io.deb.signing.key && \
gpg --import tyk.io.deb.signing.key && \
sudo /opt/tyk-dashboard/install/setup.sh --listenport=3000 --redishost=$REDIS_HOST --redisport=6379 --mongo=mongodb://$MONGO_IP/tyk_analytics --tyk_api_hostname=$HOSTNAME --tyk_node_hostname=http://localhost --tyk_node_port=8080 --portal_root=/portal --domain=$DOMAIN && \
sudo systemctl start tyk-dashboard && \
sudo systemctl enable tyk-dashboard

# Step 3: Set up our APT Repositories for Tyk Pump
curl -L https://packagecloud.io/tyk/tyk-pump/gpgkey | sudo apt-key add - && \
sudo apt-get update && \
sudo apt-get install -y apt-transport-https && \
echo "deb https://packagecloud.io/tyk/tyk-pump/ubuntu/ $UBUNTU_CODENAME main" | sudo tee /etc/apt/sources.list.d/tyk_tyk-pump.list && \
echo "deb-src https://packagecloud.io/tyk/tyk-pump/ubuntu/ $UBUNTU_CODENAME main" | sudo tee -a /etc/apt/sources.list.d/tyk_tyk-pump.list && \
sudo apt-get update && \
sudo apt-get install -y tyk-pump && \
wget https://keyserver.tyk.io/tyk.io.deb.signing.key && \
gpg --import tyk.io.deb.signing.key && \
sudo /opt/tyk-pump/install/setup.sh --redishost=$REDIS_HOST --redisport=6379 --mongo=mongodb://$MONGO_IP/tyk_analytics && \
sudo service tyk-pump start && \
sudo service tyk-pump enable

# Step 4: Set up our APT Repositories for Tyk Gateway
curl -L https://packagecloud.io/tyk/tyk-gateway/gpgkey | sudo apt-key add - && \
sudo apt-get update && \
sudo apt-get install -y apt-transport-https && \
echo "deb https://packagecloud.io/tyk/tyk-gateway/ubuntu/ $UBUNTU_CODENAME main" | sudo tee /etc/apt/sources.list.d/tyk_tyk-gateway.list && \
echo "deb-src https://packagecloud.io/tyk/tyk-gateway/ubuntu/ $UBUNTU_CODENAME main" | sudo tee -a /etc/apt/sources.list.d/tyk_tyk-gateway.list && \
sudo apt-get update && \
sudo apt-get install -y tyk-gateway && \
wget https://keyserver.tyk.io/tyk.io.deb.signing.key && \
gpg --import tyk.io.deb.signing.key && \
sudo /opt/tyk-gateway/install/setup.sh --dashboard=1 --listenport=8080 --redishost=$REDIS_HOST --redisport=6379 && \
sudo service tyk-gateway start && \
sudo service tyk-gateway enable

# Step 5: Verify services status
echo "Checking status of tyk-dashboard, tyk-pump, and tyk-gateway services..."
sudo systemctl status tyk-dashboard
sudo systemctl status tyk-pump
sudo systemctl status tyk-gateway || echo "tyk-gateway service not found"

# Step 6: Open Tyk Dashboard in Chrome
cmd.exe /C start chrome http://localhost:3000
