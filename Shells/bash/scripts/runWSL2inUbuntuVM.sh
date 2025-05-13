#!/bin/bash

# Define variables
PASSWORD="blackablacka2"
USER="micha"
HOST="192.168.1.178"
WSL_DISTRO="Ubuntu"

# Run SSH command to start WSL without hanging
sshpass -p "$PASSWORD" ssh -t $USER@$HOST 'wsl -d '"$WSL_DISTRO"
