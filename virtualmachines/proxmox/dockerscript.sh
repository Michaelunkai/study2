#!/bin/ 

# Update and upgrade system
apt update -y
apt upgrade -y
apt dist-upgrade -y

# Install Docker
apt install -y -qq docker.io

# Add user to the docker group
usermod -aG docker $USER
newgrp docker

# Start Docker service
service docker start

# Set permissions for the user on the docker socket
sh -c "setfacl -m user:$USER:rw /var/run/docker.sock"

# Update and upgrade system again (if needed)
apt update -y
apt upgrade -y
