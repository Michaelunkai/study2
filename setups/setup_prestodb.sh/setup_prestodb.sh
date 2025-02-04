#!/bin/ 

# Step 2: Install Java Development Kit (JDK)
sudo apt install openjdk-11-jdk -y
java -version

# Step 3: Download PrestoDB
wget https://repo1.maven.org/maven2/io/presto /presto-server/350/presto-server-350.tar.gz
tar -xvf presto-server-350.tar.gz
sudo mv presto-server-350 /usr/local/presto

# Step 4: Set Up the PrestoDB Configuration
sudo mkdir -p /usr/local/presto/etc

# 4.1. Node Properties
sudo bash -c 'cat > /usr/local/presto/etc/node.properties <<EOF
node.environment=production
node.id=ffffffff-ffff-ffff-ffff-ffffffffffff
node.data-dir=/var/presto/data
EOF'
sudo mkdir -p /var/presto/data

# 4.2. JVM Config
sudo bash -c 'cat > /usr/local/presto/etc/jvm.config <<EOF
-server
-Xmx16G
-XX:-UseBiasedLocking
-XX:+UseG1GC
-XX:G1HeapRegionSize=32M
-XX:+ExplicitGCInvokesConcurrent
-XX:+ExitOnOutOfMemoryError
-XX:+UseGCOverheadLimit
EOF'

# 4.3. Config Properties
sudo bash -c 'cat > /usr/local/presto/etc/config.properties <<EOF
coordinator=true
node-scheduler.include-coordinator=true
http-server.http.port=8080
query.max-memory=5GB
query.max-memory-per-node=1GB
query.max-total-memory-per-node=2GB
discovery-server.enabled=true
discovery.uri=http://localhost:8080
EOF'

# 4.4. Catalog Properties
sudo mkdir /usr/local/presto/etc/catalog
sudo bash -c 'cat > /usr/local/presto/etc/catalog/jmx.properties <<EOF
connector.name=jmx
EOF'

# Step 5: Start PrestoDB
cd /usr/local/presto
bin/launcher start

# Step 6: Using PrestoDB CLI
wget https://repo1.maven.org/maven2/io/presto /presto-cli/350/presto-cli-350-executable.jar
mv presto-cli-350-executable.jar presto
chmod +x presto
./presto --server localhost:8080 --catalog jmx --schema jmx

# Step 7: Running a Query
# Note: This step requires manual execution in the CLI

# Step 8: Stopping PrestoDB
cd /usr/local/presto
bin/launcher stop

echo "PrestoDB setup complete."
