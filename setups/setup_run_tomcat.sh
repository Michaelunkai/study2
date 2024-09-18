#!/bin/ 

# Task 1: Install Apache Tomcat Server on Ubuntu 22.04


# Step 2: Install Java
sudo apt install -y openjdk-11-jre-headless

# Step 3: Check the availability of the tomcat package
sudo apt-cache search tomcat

# Step 4: Install Apache Tomcat Server
sudo apt install -y tomcat9 tomcat9-admin

# Step 5: Check the ports for Apache Tomcat Server
ss -ltn

# Step 6 (optional): Open ports for Apache Tomcat Server
sudo ufw allow from any to any port 8080 proto tcp

# Step 7: Test working of Apache Tomcat Server
echo "Open your browser and navigate to http://localhost:8080 to verify the installation."

# Task 2: Use Apache Tomcat Web Application Manager on Ubuntu 22.04

# Step 1: Creating Tomcat user
sudo bash -c 'cat <<EOF > /etc/tomcat9/tomcat-users.xml
<tomcat-users>
    <role rolename="manager-gui"/>
    <role rolename="admin-gui"/>
    <user username="tomcat" password="helloworld" roles="manager-gui,admin-gui"/>
</tomcat-users>
EOF'

# Ensure the file has the correct permissions
sudo chmod 640 /etc/tomcat9/tomcat-users.xml
sudo chown root:tomcat /etc/tomcat9/tomcat-users.xml

# Step 2: Restart Tomcat Server
sudo systemctl restart tomcat9

echo "Open your browser and navigate to http://localhost:8080/manager/html and log in with username 'tomcat' and password 'helloworld'."

# Step 3: Change the Apache Tomcat port number
sudo sed -i 's/Connector port="8080"/Connector port="9090"/' /etc/tomcat9/server.xml

# Restart Tomcat to apply the port change
sudo systemctl restart tomcat9

echo "Tomcat port changed to 9090. Open your browser and navigate to http://localhost:9090 to access Tomcat."

# Open the Tomcat Web Application Manager in Chrome (only works on Windows)
cmd.exe /c start chrome http://localhost:9090/manager/html
