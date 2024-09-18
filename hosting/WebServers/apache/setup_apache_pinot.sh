#!/bin/ 

# Step 1: Installing Java
if ! java -version &> /dev/null; then
  if [ -f /etc/debian_version ]; then
    sudo apt-get update && sudo apt-get install default-jdk -y
  elif [ -f /etc/redhat-release ]; then
    sudo dnf install java-21-openjdk -y
  else
    echo "Unsupported Linux distribution"
    exit 1
  fi
fi
java -version

# Step 2: Installing Zookeeper
if [ -f /etc/debian_version ]; then
  sudo apt install zookeeperd -y
elif [ -f /etc/redhat-release ]; then
  sudo dnf install zookeeperd -y
else
  echo "Unsupported Linux distribution"
  exit 1
fi

sudo systemctl start zookeeper
sudo systemctl enable zookeeper
sudo systemctl status zookeeper

# Step 3: Installing Apache Pinot
PINOT_VERSION="1.1.0"
wget https://downloads.apache.org/pinot/apache-pinot-${PINOT_VERSION}/apache-pinot-${PINOT_VERSION}-bin.tar.gz
sudo tar -xvzf apache-pinot-${PINOT_VERSION}-bin.tar.gz -C /opt
echo "export PINOT_HOME=/opt/apache-pinot-${PINOT_VERSION}-bin" >> ~/.bashrc
echo 'export PATH=$PINOT_HOME/bin:$PATH' >> ~/.bashrc
source ~/. rc

# Ensure environment variables are updated
export PINOT_HOME=/opt/apache-pinot-${PINOT_VERSION}-bin
export PATH=$PINOT_HOME/bin:$PATH

# Step 4: Starting Apache Pinot Services
cd $PINOT_HOME
nohup bin/pinot-admin.sh StartController -configFileName conf/pinot-controller.conf &
nohup bin/pinot-admin.sh StartBroker -configFileName conf/pinot-broker.conf &
nohup bin/pinot-admin.sh StartServer -configFileName conf/pinot-server.conf &
nohup bin/pinot-admin.sh StartMinion -configFileName conf/pinot-minion.conf &

sleep 10 # Allow some time for services to start

# Step 5: Configuring Apache Pinot
sudo mkdir -p $PINOT_HOME/configs

# Creating schema file
sudo tee $PINOT_HOME/configs/my_schema.json > /dev/null <<EOL
{
  "schemaName": "mySchema",
  "dimensionFieldSpecs": [
    {
      "name": "myDimension",
      "dataType": "STRING"
    }
  ],
  "metricFieldSpecs": [
    {
      "name": "myMetric",
      "dataType": "LONG"
    }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "myDateTime",
      "dataType": "LONG",
      "format": "1:MILLISECONDS:EPOCH",
      "granularity": "1:MILLISECONDS"
    }
  ]
}
EOL

# Creating table configuration file
sudo tee $PINOT_HOME/configs/my_table.json > /dev/null <<EOL
{
  "tableName": "myTable",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "myDateTime",
    "schemaName": "mySchema",
    "replication": "1"
  },
  "tableIndexConfig": {
    "loadMode": "MMAP"
  },
  "tenants": {},
  "tableRetentionConfig": {},
  "ingestionConfig": {
    "streamIngestionConfig": {
      "type": "kafka",
      "streamConfigMaps": {
        "streamType": "kafka",
        "stream.kafka.topic.name": "myKafkaTopic",
        "stream.kafka.broker.list": "localhost:9092",
        "stream.kafka.consumer.type": "simple",
        "stream.kafka.consumer.prop.auto.offset.reset": "smallest",
        "realtime.segment.flu .thre old.size": "50000"
      }
    }
  },
  "metadata": {}
}
EOL

# Adding schema and table configurations
bin/pinot-admin.sh AddSchema -schemaFile $PINOT_HOME/configs/my_schema.json -controllerProtocol http -controllerHost localhost -controllerPort 9000 -exec
bin/pinot-admin.sh AddTable -tableConfigFile $PINOT_HOME/configs/my_table.json -controllerProtocol http -controllerHost localhost -controllerPort 9000 -exec

# Open Chrome browser to Pinot Controller UI
cmd.exe /c start chrome http://localhost:9000
