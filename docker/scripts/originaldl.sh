#!/bin/bash

# Your Docker Hub username and password
username="michadockermisha"
password="Aa111111!"

# Log in to Docker Hub
echo "$password" | docker login --username "$username" --password-stdin
