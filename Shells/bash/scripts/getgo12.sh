#!/bin/bash

# Script to install Go version 1.12.17, set up the environment, and ensure it works in the current shell without refreshing.

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

# Download and install Go version 1.12.17
wget https://go.dev/dl/go1.12.17.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.12.17.linux-amd64.tar.gz
rm go1.12.17.linux-amd64.tar.gz

# Update PATH for the new Go installation
export PATH=/usr/local/go/bin:$PATH
echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc

# Apply the changes to the current shell immediately
source ~/.bashrc

# Verify Go installation
go version
if [[ $(go version) != *"go1.12.17"* ]]; then
    echo "Error: Go version is not 1.12.17. Exiting."
    exit 1
fi

# Initialize a new Go module
if [ ! -f "go.mod" ]; then
    go mod init new
else
    echo "Go module already initialized. Skipping."
fi

# Install golint and other Go-related packages
go install golang.org/x/lint/golint@latest
go install github.com/fatih/gomodifytags@latest
go install github.com/go-delve/delve/cmd/dlv@latest

# Update PATH for Go tools
export PATH=$(go env GOPATH)/bin:$PATH
echo 'export PATH=$(go env GOPATH)/bin:$PATH' >> ~/.bashrc

# Apply the changes to the current shell immediately
source ~/.bashrc

# Final confirmation
echo "Go version $(go version) installed and environment configured successfully."

# Display installed Go version
go version
