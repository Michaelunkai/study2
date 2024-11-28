#!/bin/bash

# Proxmox VM ID
VM_ID=101

# VM Storage Path
VM_STORAGE_PATH="/var/lib/vz/images/$VM_ID"

# Check if the VM exists
if [ ! -d "$VM_STORAGE_PATH" ]; then
  echo "Error: VM ID $VM_ID does not exist in $VM_STORAGE_PATH."
  exit 1
fi

# Step 1: Shutdown the VM
echo "Shutting down VM $VM_ID..."
qm shutdown $VM_ID
while qm status $VM_ID | grep -q "running"; do
  echo "Waiting for VM to shut down..."
  sleep 5
done
echo "VM $VM_ID has been shut down."

# Step 2: Mount the disk in the VM and zero unused space
echo "Booting VM $VM_ID to zero out unused space..."
qm start $VM_ID
sleep 10

echo "Zeroing unused space in VM $VM_ID..."
qm guest exec $VM_ID -- bash -c 'dd if=/dev/zero of=/zero.fill bs=1M || rm -f /zero.fill'
echo "Unused space zeroed inside VM $VM_ID."

# Shutdown the VM again after zeroing
echo "Shutting down VM $VM_ID again..."
qm shutdown $VM_ID
while qm status $VM_ID | grep -q "running"; do
  echo "Waiting for VM to shut down..."
  sleep 5
done
echo "VM $VM_ID is now offline."

# Step 3: Compress the disk image
echo "Compressing the disk image for VM $VM_ID..."
DISK_IMAGE=$(find $VM_STORAGE_PATH -name "*.raw" -or -name "*.qcow2" | head -n 1)
if [ -z "$DISK_IMAGE" ]; then
  echo "Error: No disk image found for VM $VM_ID."
  exit 1
fi

COMPRESSED_IMAGE="$VM_STORAGE_PATH/compressed-disk-$VM_ID.qcow2"
echo "Disk image located: $DISK_IMAGE"
echo "Converting and compressing the image..."
qemu-img convert -O qcow2 $DISK_IMAGE $COMPRESSED_IMAGE

# Step 4: Replace the old disk image with the compressed one
echo "Replacing the old disk image with the compressed image..."
mv $COMPRESSED_IMAGE $DISK_IMAGE
echo "Disk image replaced successfully."

# Step 5: Start the VM again
echo "Starting VM $VM_ID..."
qm start $VM_ID
echo "VM $VM_ID has been started."

# Step 6: Verify reclaimed space
echo "Verifying disk space on Proxmox host..."
du -sh $VM_STORAGE_PATH
echo "Free space has been reclaimed successfully!"

# Completion message
echo "Disk cleanup and compression for VM $VM_ID completed."
