#!/bin/bash
# Script to remove existing VM 101 and restore it from the latest backup

# Set variables
VM_ID=101
BACKUP_DIR="/var/lib/vz/dump" # Default backup directory for Proxmox
STORAGE="local"              # Storage ID where backups are stored
RESTORE_ID=101               # ID for the restored VM (use same as original if replacing)

# Find the latest backup for the specified VM
LATEST_BACKUP=$(ls -t ${BACKUP_DIR}/vzdump-qemu-${VM_ID}-*.{tar,zst} 2>/dev/null | head -n 1)

# Check if a backup file was found
if [ -z "$LATEST_BACKUP" ]; then
    echo "No backup found for VM $VM_ID in $BACKUP_DIR."
    exit 1
fi

echo "Latest backup found: $LATEST_BACKUP"

# Remove the existing VM if it exists
if qm list | grep -q "^\\s*${VM_ID}\\s"; then
    echo "VM $VM_ID already exists. Removing it..."
    qm stop $VM_ID >/dev/null 2>&1
    qm destroy $VM_ID --purge >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "VM $VM_ID successfully removed."
    else
        echo "Failed to remove VM $VM_ID."
        exit 1
    fi
fi

# Restore the VM
echo "Restoring VM $VM_ID from $LATEST_BACKUP..."
qmrestore $LATEST_BACKUP $RESTORE_ID --storage $STORAGE

# Check if the restoration was successful
if [ $? -eq 0 ]; then
    echo "VM $VM_ID restored successfully from $LATEST_BACKUP."
    # Start the VM
    echo "Starting VM $VM_ID..."
    qm start $VM_ID
    if [ $? -eq 0 ]; then
        echo "VM $VM_ID started successfully."
    else
        echo "Failed to start VM $VM_ID."
        exit 1
    fi
else
    echo "Failed to restore VM $VM_ID."
    exit 1
fi
