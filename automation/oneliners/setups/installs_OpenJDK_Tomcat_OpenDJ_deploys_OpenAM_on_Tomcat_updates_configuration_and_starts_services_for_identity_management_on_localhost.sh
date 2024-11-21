#!/bin/ 

# Change to root directory
cd /root

# Install necessary packages
sudo apt-get install -y openjdk-11-jdk unzip tomcat9

# Download OpenAM WAR file
wget https://github.com/OpenIdentityPlatform/OpenAM/releases/download/14.6.4/OpenAM-14.6.4.war -O openam.war

# Set environment variables
TOMCAT_PATH="/var/lib/tomcat9"
OPENDJ_PATH="/opt/opendj"
DJ_HOSTNAME="localhost"

# Step 1: Install OpenDJ
echo "Installing OpenDJ..."
# Download correct OpenDJ package
wget https://github.com/OpenIdentityPlatform/OpenDJ/releases/download/4.4.11/OpenDJ-4.4.11.zip -O /tmp/opendj.zip
# Extract OpenDJ package
unzip /tmp/opendj.zip -d /opt/

# Run OpenDJ setup
$OPENDJ_PATH/setup <<EOF
1
password
password
y
$DJ_HOSTNAME
y
1
cn=Directory Manager
password
password
1
yes
yes
no
yes
2
EOF

# Check the OpenDJ status
$OPENDJ_PATH/bin/status --offline

# Step 2: Update Tomcat to run on port 8085
echo "Updating Tomcat port to 8085..."
sed -i "s/port=\"8080\"/port=\"8085\"/g" $TOMCAT_PATH/conf/server.xml

# Step 3: Deploy OpenAM on Tomcat
echo "Deploying OpenAM..."
cp openam.war $TOMCAT_PATH/webapps/sso.war

# Update hosts file for OpenAM and OpenDJ access
echo "Updating hosts file..."
echo "127.0.0.1 localhost" | sudo tee -a /etc/hosts

# Start Tomcat service
systemctl start tomcat9
