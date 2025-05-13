#!/bin/bash

# Define an array of VM IP addresses
VM_IPS=("192.168.1.193" "192.168.1.194" "192.168.1.195") # Add all your VM IPs here

# Define SSH username and password
SSH_USER="ubuntu"
SSH_PASS="123456"

# Loop through each VM and execute update and upgrade commands
for VM_IP in "${VM_IPS[@]}"; do
    echo "Updating VM at $VM_IP..."
    sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no "$SSH_USER@$VM_IP" \
    "echo \"$SSH_PASS\" | sudo -S apt update && echo \"$SSH_PASS\" | sudo -S apt upgrade -y"

    if [ $? -eq 0 ]; then
        echo "Successfully updated VM at $VM_IP."
    else
        echo "Failed to update VM at $VM_IP."
    fi
    echo "----------------------------------------"
done

echo "All updates completed."
