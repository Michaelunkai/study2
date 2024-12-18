#!/bin/bash

# ========================================================================
# Script to Install ttyd and Cloudflared on WSL with Background Execution
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

# Install Cloudflared
echo_separator
echo "Installing Cloudflared..."
echo_separator
if ! command -v cloudflared &> /dev/null; then
    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
    sudo mv cloudflared /usr/local/bin/cloudflared
    sudo chmod +x /usr/local/bin/cloudflared
fi

# Start Cloudflared Tunnel
echo_separator
echo "Starting Cloudflared Tunnel..."
echo_separator
nohup cloudflared tunnel --url http://localhost:7681 > ~/cloudflared.log 2>&1 &
CLOUDFLARED_PID=$!
echo "Cloudflared started with PID: $CLOUDFLARED_PID"

# Wait for Cloudflared to initialize
echo_separator
echo "Waiting for Cloudflared to Initialize..."
echo_separator
sleep 10  # Allow Cloudflared time to start up

# Fetch the public URL from Cloudflared log
echo_separator
echo "Fetching Cloudflared Public URL..."
echo_separator
PUBLIC_URL=$(grep -oP '(?<=https://)[^ ]+\.trycloudflare\.com' ~/cloudflared.log | head -1)
if [ -z "$PUBLIC_URL" ]; then
    echo "Failed to retrieve Cloudflared public URL. Check logs."
    exit 1
fi
PUBLIC_URL="https://$PUBLIC_URL"

# Stop timer
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Output results
echo_separator
echo "Cloudflared Tunnel Established"
echo "Public URL: $PUBLIC_URL"
echo_separator
echo "Script Execution Completed"
echo "Public URL: $PUBLIC_URL"
echo "Total Execution Time: $DURATION seconds"
echo_separator

# Exit the script, returning to the shell while keeping ttyd and Cloudflared running
exit 0
