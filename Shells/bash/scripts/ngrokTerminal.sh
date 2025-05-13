#!/bin/bash

# ========================================================================
# Script to Install ttyd and ngrok on WSL with Background Execution
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
    apt-transport-https

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
make
sudo make install

# Start ttyd in background using nohup to ensure it keeps running after script exits
echo_separator
echo "Starting ttyd in Background..."
echo_separator
nohup ttyd --writable bash > ~/ttyd.log 2>&1 &
TTYD_PID=$!
echo "ttyd started with PID: $TTYD_PID"

# Install Node.js and npm using the provided one-liner
echo_separator
echo "Installing Node.js and npm..."
echo_separator
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && \
sudo apt-get install -y nodejs=22.1.0-1nodesource1 && \
npm install -g npm@latest && \
node -v && npm -v

# Install ngrok
echo_separator
echo "Installing ngrok..."
echo_separator
sudo npm install -g ngrok

# Configure ngrok with your authtoken
echo_separator
echo "Configuring ngrok..."
echo_separator
ngrok config add-authtoken 2pRcoJEfKjWvAu2zHDAmHA1caui_7NRu838gBdijqdv8TeuM3

# Start ngrok in background using nohup
echo_separator
echo "Starting ngrok Tunnel..."
echo_separator
nohup ngrok http 7681 > ~/ngrok.log 2>&1 &
NGROK_PID=$!
echo "ngrok started with PID: $NGROK_PID"

# Wait for ngrok to initialize
echo_separator
echo "Waiting for ngrok to Initialize..."
echo_separator
sleep 10  # Adjust if necessary based on your network speed

# Get the public URL from ngrok
echo_separator
echo "Fetching ngrok Public URL..."
echo_separator
PUBLIC_URL=$(curl --silent http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# Stop timer
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Output results
echo_separator
echo "ngrok Tunnel Established"
echo "Public URL: $PUBLIC_URL"
echo_separator
echo "Script Execution Completed"
echo "Public URL: $PUBLIC_URL"
echo "Total Execution Time: $DURATION seconds"
echo_separator

# Exit the script, returning to the shell while keeping ttyd and ngrok running
exit 0
