#!/bin/ 

set -e  # Exit immediately if a command exits with a non-zero status

# Install jq if not present
if ! command -v jq &> /dev/null
then
    echo "jq not found, installing..."
    sudo apt-get update
    sudo apt-get install -y jq
fi

# Fetch the latest version tag
_v=$(curl -s "https://api.github.com/repos/kubernetes/kompose/releases/latest" | jq -r .tag_name)

# Check if version was fetched
if [[ -z "$_v" ]]; then
    echo "Failed to fetch the latest version."
    exit 1
fi

echo "Latest kompose version: $_v"

# Download kompose
curl -L "https://github.com/kubernetes/kompose/releases/download/$_v/kompose-linux-amd64" -o kompose

# Make it executable
chmod +x kompose

# Move to /usr/local/bin
sudo mv ./kompose /usr/local/bin/kompose

# Verify installation
kompose version
