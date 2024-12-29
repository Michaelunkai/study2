#!/bin/bash

# Remove any existing Go installation
sudo rm -rf /usr/local/go
sudo rm -rf /root/go
sudo rm -rf /root/go.mod

# Clean up old PATH entries
sed -i '/\/usr\/local\/go\/bin/d' ~/.bashrc
sed -i '/$(go env GOPATH)\/bin/d' ~/.bashrc

# Navigate to the home directory
cd

# Download and install the specified Go version
wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz

# Update PATH to include the new Go installation
export PATH=/usr/local/go/bin:$PATH
echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc

# Reload .bashrc to apply changes
source ~/.bashrc

# Verify Go version
go version

# Ensure Go version is correct
if [[ $(go version) != *"go1.23.4"* ]]; then
    echo "Error: Go version is not 1.23.4. Exiting."
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

echo "Go installation and environment setup completed successfully."

