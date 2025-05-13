#!/bin/bash

# Variables
VMID="101"
STORAGE="local"
COMPRESSION="zstd"
MODE="snapshot"
BACKUP_NOTES="Ubuntu_Desktop"

# Delete all existing backups for VMID 101
echo "Deleting existing backups for VM $VMID..."
BACKUP_PATH="/var/lib/vz/dump"
if [ -d "$BACKUP_PATH" ]; then
    BACKUP_FILES=$(ls "$BACKUP_PATH" | grep "qemu-$VMID-")
    for FILE in $BACKUP_FILES; do
        rm -f "$BACKUP_PATH/$FILE"
        echo "Deleted: $FILE"
    done
else
    echo "Backup path $BACKUP_PATH does not exist!"
    exit 1
fi

# Create a new backup
echo "Creating new backup for VM $VMID..."
if command -v vzdump > /dev/null; then
    vzdump $VMID \
        --storage $STORAGE \
        --compress $COMPRESSION \
        --mode $MODE \
        --notes "$BACKUP_NOTES"
    echo "Backup completed successfully!"
else
    echo "Error: 'vzdump' command not found. Ensure Proxmox is correctly installed and 'vzdump' is in your PATH."
    exit 1
fi
