#!/bin/bash

# ========================================================================
# Script to Install ttyd and localtunnel on WSL with Background Execution
# Fixing 502 Bad Gateway and ensuring service availability
# ========================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# Start timer
START_TIME=$(date +%s)

# Function to print messages with a separator
echo_separator() {
    echo "========================================"
}

# Install dependencies
echo_separator
echo "Installing Dependencies..."
echo_separator
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    cmake \
    git \
    libjson-c-dev \
    libwebsockets-dev \
    jq \
    curl \
    wget \
    apt-transport-https \
    libssl-dev \
    zlib1g-dev \
    net-tools

# Clone and build ttyd
echo_separator
echo "Cloning and Building ttyd..."
echo_separator
cd ~
if [ ! -d "ttyd" ]; then
    git clone https://github.com/tsl0922/ttyd.git
else
    echo "ttyd repository already exists. Pulling latest changes."
    cd ttyd
    git pull
    cd ..
fi

cd ttyd
mkdir -p build
cd build
cmake ..
make -j$(nproc)
sudo make install

# Check and kill any processes already running on port 7681
if sudo lsof -i :7681; then
    echo_separator
    echo "Port 7681 is in use. Killing process..."
    sudo fuser -k 7681/tcp
fi

# Start ttyd in background using nohup
echo_separator
echo "Starting ttyd in Background..."
echo_separator
nohup ttyd --writable --port 7681 bash > ~/ttyd.log 2>&1 &
TTYD_PID=$!
sleep 2

# Verify ttyd is running
if ! sudo lsof -i :7681 > /dev/null; then
    echo "Error: ttyd failed to start on port 7681"
    exit 1
fi
echo "ttyd started successfully with PID: $TTYD_PID"

# Install Node.js and npm
echo_separator
echo "Installing Node.js and npm..."
echo_separator
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
npm install -g npm@11.0.0 --force

# Install localtunnel
echo_separator
echo "Installing localtunnel..."
echo_separator
sudo npm install -g localtunnel

# Start localtunnel in background using nohup
echo_separator
echo "Starting localtunnel Tunnel..."
echo_separator
nohup lt --port 7681 > ~/localtunnel.log 2>&1 &
LT_PID=$!
sleep 5

# Verify localtunnel is running
if ! ps -p $LT_PID > /dev/null; then
    echo "Error: localtunnel failed to start"
    exit 1
fi
echo "localtunnel started successfully with PID: $LT_PID"

# Wait for localtunnel to initialize and fetch the public URL
echo_separator
echo "Fetching localtunnel Public URL..."
echo_separator
sleep 5
PUBLIC_URL=$(grep -oP '(?<=your url is: ).*' ~/localtunnel.log | tail -n1)

if [[ -z "$PUBLIC_URL" ]]; then
    echo "Error: Failed to fetch localtunnel public URL"
    exit 1
fi

# Stop timer
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Output results
echo_separator
echo "localtunnel Tunnel Established"
echo "Public URL: $PUBLIC_URL"
echo_separator
echo "Script Execution Completed"
echo "Public URL: $PUBLIC_URL"
echo "Total Execution Time: $DURATION seconds"
echo_separator

# Execute wget command using the public URL
echo_separator
echo "Fetching password with wget command..."
echo_separator
wget -q -O - "${PUBLIC_URL}/mytunnelpassword"

# Exit the script
exit 0
