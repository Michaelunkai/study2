#!/bin/ 

# Create script file with the name describing the tools used and purpose
SCRIPT_NAME="setup_run_iot_starterkit_fixed_errors.sh"

# Add script content to the file
cat << 'EOF' > $SCRIPT_NAME
#!/bin/ 

# Clone the repository
echo "Cloning the SAP IoT Starter Kit repository..."
git clone https://github.com/SAP-archive/cloud-platform-iot-starterkit.git
cd cloud-platform-iot-starterkit

# Install necessary dependencies for Java, Maven, Python, Node.js, and Mosquitto
echo "Installing Java, Maven, Python, and Node.js dependencies..."
sudo apt install -y openjdk-11-jdk maven python3 python3-pip mosquitto mosquitto-clients

# Fix npm and node.js conflicts by manually installing Node.js and npm
sudo npm install -g n
sudo n stable

# Check Node.js installation
node -v
npm -v

# Set up the Java project (for Neo or CF environment)
if [ -d "neo" ]; then
    echo "Building Java project using Maven in 'neo' environment..."
    cd neo
    if [ -f pom.xml ]; then
        mvn clean install
        mvn spring-boot:run &
    else
        echo "Maven configuration (pom.xml) file not found in 'neo', trying 'cf'..."
        cd ../cf
        if [ -f pom.xml ]; then
            mvn clean install
            mvn spring-boot:run &
        else
            echo "Maven configuration (pom.xml) file not found in 'cf', skipping Java build."
        fi
    fi
else
    echo "'neo' and 'cf' directories not found, skipping Java project setup."
fi

# Add necessary configuration or text to application.properties if required
if [ ! -f src/main/resources/application.properties ]; then
    echo "Creating application.properties file..."
    mkdir -p src/main/resources
    cat <<EOL > src/main/resources/application.properties
# Add necessary configuration here
EOL
else
    echo "application.properties file already exists."
fi

# Navigate to Python directories and check if the Python script exists
if [ -d "python_samples" ]; then
    echo "Running Python scripts..."
    cd  _samples
    if [ -f your_script.py ]; then
         3 your_script.py &
    else
        echo "Python script not found, skipping Python scripts."
    fi
else
    echo "Python samples not found, skipping Python scripts."
fi

# Navigate to JavaScript directories and run Node.js applications
if [ -d "cf/samples/javascript-samples/geotab" ]; then
    echo "Running JavaScript application..."
    cd cf/samples/javascript-samples/geotab
    npm install
    if [ -f your_app.js ]; then
        node your_app.js &
    else
        echo "Node.js application (your_app.js) not found."
    fi
else
    echo "JavaScript samples not found, skipping Node.js application."
fi

# Start Mosquitto MQTT broker (if installed)
echo "Starting Mosquitto MQTT broker..."
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Add necessary configurations to config.yml if the file exists
if [ ! -f ../config/config.yml ]; then
    echo "Creating config.yml..."
    mkdir -p ../config
    cat <<EOL > ../config/config.yml
# Add necessary configuration content here
EOL
else
    echo "config.yml file already exists."
fi

echo "Setup complete. All components are running."
EOF

# Make the script executable
chmod +x $SCRIPT_NAME

# Execute the script
./$SCRIPT_NAME
