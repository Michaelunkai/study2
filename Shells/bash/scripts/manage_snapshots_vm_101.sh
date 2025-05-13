#!/bin/bash

# Variables
VMID="101"
SNAPSHOT_NAME="new-snapshot"

# Delete all existing snapshots for VMID 101
echo "Deleting all snapshots for VM $VMID..."
SNAPSHOTS=$(qm listsnapshots $VMID | awk 'NR>1 {print $1}') # Fetch list of snapshots excluding the header
if [ -z "$SNAPSHOTS" ]; then
    echo "No snapshots found for VM $VMID."
else
    for SNAPSHOT in $SNAPSHOTS; do
        echo "Deleting snapshot: $SNAPSHOT"
        qm delsnapshot $VMID $SNAPSHOT
    done
    echo "All snapshots deleted for VM $VMID."
fi

# Create a new snapshot
echo "Creating a new snapshot for VM $VMID..."
qm snapshot $VMID $SNAPSHOT_NAME --description "Auto-created snapshot on $(date)"
if [ $? -eq 0 ]; then
    echo "Snapshot '$SNAPSHOT_NAME' created successfully for VM $VMID."
else
    echo "Failed to create snapshot for VM $VMID."
    exit 1
fi
