#!/bin/bash

# Update PATH and install necessary packages
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:$PATH
apt update
apt install -y openjdk-11-jdk wget tar

# Download and extract Apache Zeppelin
wget https://downloads.apache.org/zeppelin/zeppelin-0.10.1/zeppelin-0.10.1-bin-all.tgz
tar -xvf zeppelin-0.10.1-bin-all.tgz
mv zeppelin-0.10.1-bin-all /opt/zeppelin

# Create necessary directories
mkdir -p /opt/zeppelin/logs /opt/zeppelin/pid /opt/zeppelin/conf

# Create zeppelin-env.sh
cat <<EOL > /opt/zeppelin/conf/zeppelin-env.sh
export ZEPPELIN_JAVA_OPTS="-Dzeppelin.server.addr=0.0.0.0"
export HADOOP_CONF_DIR=""
export ZEPPELIN_LOG_DIR=/opt/zeppelin/logs
export ZEPPELIN_PID_DIR=/opt/zeppelin/pid
EOL

# Create zeppelin-site.xml
cat <<EOL > /opt/zeppelin/conf/zeppelin-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>zeppelin.server.port</name>
    <value>8082</value>
  </property>
</configuration>
EOL

# Update bashrc with Zeppelin environment variables
echo 'export ZEPPELIN_HOME=/opt/zeppelin' >> ~/.bashrc
echo 'export PATH=$PATH:$ZEPPELIN_HOME/bin' >> ~/.bashrc

# Reload bashrc
source ~/.bashrc

# Print access information
echo "Zeppelin is ready. Access it at: http://localhost:8082"
