#!/bin/bash

# Your Docker Hub username and password
username="michadockermisha"
password="Aa111111!"

# Docker saved path
docker_path="/mnt/d/docker"

# Log in to Docker Hub
echo "$password" | docker login --username "$username" --password-stdin

# Change to the Docker saved path
cd "$docker_path"

# Additional commands if needed
# ...

# Example: List Docker containers in the saved path
docker ps
