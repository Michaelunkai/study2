#!/bin/ 

# Install MariaDB server
sudo apt-get install -y mariadb-server

# Create Jira database and user
sudo mariadb -u root -e "DROP DATABASE IF EXISTS jiradb; CREATE DATABASE jiradb CHARACTER SET utf8mb4 COLLATE utf8mb4_bin; CREATE USER IF NOT EXISTS 'jirauser'@'localhost' IDENTIFIED BY '123456'; GRANT ALL PRIVILEGES ON jiradb.* TO 'jirauser'@'localhost'; FLUSH PRIVILEGES;"

# Download Jira software
cd ~
wget https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-9.12.0-x64.bin

# Make Jira installer executable
chmod a+x atlassian-jira-software-9.12.0-x64.bin

# Run Jira installer
sudo ./atlassian-jira-software-9.12.0-x64.bin

# Download MariaDB Java connector
wget https://downloads.mariadb.com/Connectors/java/connector-java-2.7.4/mariadb-java-client-2.7.4.jar

# Copy MariaDB Java connector to Jira lib directory
sudo cp mariadb-java-client-2.7.4.jar /opt/atlassian/jira/lib/

# Stop and start Jira service
sudo /etc/init.d/jira stop
sudo /etc/init.d/jira start

# Open Jira in Chrome using cmd.exe in WSL
cmd.exe /c start chrome http://localhost:8080
