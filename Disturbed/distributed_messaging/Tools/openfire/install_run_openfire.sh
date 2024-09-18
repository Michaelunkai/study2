#!/bin/ 

# Step 1 — Keep the server updated
echo "Updating the server..."
sudo apt update -y && sudo apt upgrade -y

# Step 2 — Install Java
echo "Installing OpenJDK 11..."
sudo apt install openjdk-11-jre -y

# Set up JAVA_HOME environment variable
echo "Setting up JAVA_HOME environment variable..."
echo "JAVA_HOME=$(readlink -f /usr/bin/java | sed 's:bin/java::')" | sudo tee -a /etc/profile
source /etc/profile

# Step 3 — Install latest Openfire
echo "Downloading and installing Openfire..."
cd /tmp
wget -O openfire_4.6.2_all.deb https://www.igniterealtime.org/downloadServlet?filename=openfire/openfire_4.6.2_all.deb
sudo apt install ./openfire_4.6.2_all.deb -y

# Step 4 — Install MariaDB database for Openfire
echo "Installing MariaDB..."
curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
sudo apt install mariadb-server mariadb-client -y

echo "Securing MariaDB installation..."
sudo my _secure_installation <<EOF

Y
your-MariaDB-root-password
your-MariaDB-root-password
Y
Y
Y
Y
EOF

echo "Creating a dedicated database for Openfire..."
sudo mysql -u root -pyour-MariaDB-root-password <<EOF
CREATE DATABASE openfire;
CREATE USER 'openfireuser'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON openfire.* TO 'openfireuser'@'localhost' IDENTIFIED BY 'yourpassword' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EXIT;
EOF

# Starting Openfire service
echo "Starting and enabling Openfire service..."
sudo systemctl start openfire
sudo systemctl enable openfire

# Open Openfire admin console in Chrome
echo "Opening Openfire admin console in Chrome..."
cmd.exe /c start chrome http://localhost:9090

echo "Openfire installation and setup completed!"
echo "You can access the Openfire admin console at http://your_server_ip:9090"
