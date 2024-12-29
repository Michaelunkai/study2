#!/bin/bash

# Remove any existing Go installation
sudo rm -rf /usr/local/go
sudo rm -rf ~/go
sudo rm -rf ~/go.mod

# Clean up old PATH entries from .bashrc
sed -i '/\/usr\/local\/go\/bin/d' ~/.bashrc
sed -i '/$(go env GOPATH)\/bin/d' ~/.bashrc

# Navigate to the home directory
cd

# Download and install Go version 1.22.0
wget https://go.dev/dl/go1.22.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.linux-amd64.tar.gz

# Update PATH to include the new Go installation
export PATH=/usr/local/go/bin:$PATH
echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc

# Reload .bashrc to apply changes
source ~/.bashrc

# Verify Go version
go version

# Ensure Go version is correct
if [[ $(go version) != *"go1.22.0"* ]]; then
    echo "Error: Go version is not 1.22.0. Exiting."
    exit 1
fi

# Reinitialize a Go module
go mod init new || echo "Go module already initialized. Skipping."

# Install golint and update PATH for Go tools
go install golang.org/x/lint/golint@latest
export PATH=$(go env GOPATH)/bin:$PATH
echo 'export PATH=$(go env GOPATH)/bin:$PATH' >> ~/.bashrc

# Reload .bashrc to apply updates
source ~/.bashrc

echo "Go version 1.22.0 installation and environment setup completed successfully."
