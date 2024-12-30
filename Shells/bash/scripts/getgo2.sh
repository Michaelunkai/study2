#!/bin/bash

# Script to install Go version 1.2.2, set up the environment, and ensure it works in the current shell without refreshing.

# Update and install necessary packages
sudo apt update
sudo apt install build-essential golang go -y

# Remove any existing Go installation
sudo rm -rf /usr/local/go
sudo rm -rf ~/go
sudo rm -f ~/.bashrc.bak

# Clean up old PATH entries in .bashrc
sed -i.bak '/\/usr\/local\/go\/bin/d' ~/.bashrc
sed -i '/$(go env GOPATH)\/bin/d' ~/.bashrc

# Navigate to the home directory
cd ~

# Download and install Go version 1.2.2
wget https://go.dev/dl/go1.2.2.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.2.2.linux-amd64.tar.gz
rm go1.2.2.linux-amd64.tar.gz

# Update PATH for the new Go installation
export PATH=/usr/local/go/bin:$PATH
echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc

# Apply the changes to the current shell immediately
source ~/.bashrc

# Verify Go installation
go version
if [[ $(go version) != *"go1.2.2"* ]]; then
    echo "Error: Go version is not 1.2.2. Exiting."
    exit 1
fi

# Final confirmation
echo "Go version $(go version) installed and environment configured successfully."

# Display installed Go version
go version
