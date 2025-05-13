#!/bin/bash

echo "Starting cleanup in /mnt/wslg..."

# Step 1: Check if /mnt/wslg is writable
if ! mount | grep -q "/mnt/wslg .*ro,"; then
    echo "Filesystem is mounted as read-only. Attempting to remount as read-write..."
    if sudo mount -o remount,rw /mnt/wslg; then
        echo "Remounted as read-write successfully."
    else
        echo "Failed to remount as read-write. Cleanup will be limited to read-only operations."
    fi
fi

# Step 2: Find and list large files
echo "Listing files larger than 100MB in /mnt/wslg (read-only mode)..."
sudo find /mnt/wslg -type f -size +100M -exec ls -lh {} \;

# Step 3: Attempt to remove large files (if writable)
if mount | grep -q "/mnt/wslg .*rw,"; then
    echo "Deleting files larger than 100MB in /mnt/wslg..."
    sudo find /mnt/wslg -type f -size +100M -exec rm -i {} \;
else
    echo "Skipping file deletions as filesystem is still read-only."
fi

# Step 4: Handle temporary and log files
echo "Clearing temporary and log files in /mnt/wslg (if writable)..."
if mount | grep -q "/mnt/wslg .*rw,"; then
    sudo find /mnt/wslg -type f \( -name "*.tmp" -o -name "*.log" \) -exec rm -rf {} \;
else
    echo "Skipping temporary and log file cleanup due to read-only filesystem."
fi

# Step 5: Remove empty directories
echo "Removing empty directories in /mnt/wslg (if writable)..."
if mount | grep -q "/mnt/wslg .*rw,"; then
    sudo find /mnt/wslg -type d -empty -exec rmdir {} \;
else
    echo "Skipping empty directory removal due to read-only filesystem."
fi

# Step 6: Attempt to identify orphaned or unnecessary files
echo "Listing orphaned or unnecessary files in /mnt/wslg..."
sudo find /mnt/wslg -type f \( -name "*.old" -o -name "*.bak" \) -exec ls -lh {} \;

if mount | grep -q "/mnt/wslg .*rw,"; then
    echo "Deleting orphaned or unnecessary files..."
    sudo find /mnt/wslg -type f \( -name "*.old" -o -name "*.bak" \) -exec rm -rf {} \;
else
    echo "Skipping deletion of orphaned files due to read-only filesystem."
fi

# Final Message
if mount | grep -q "/mnt/wslg .*rw,"; then
    echo "Cleanup in /mnt/wslg completed successfully!"
else
    echo "Cleanup in /mnt/wslg completed with limitations due to read-only filesystem."
fi
