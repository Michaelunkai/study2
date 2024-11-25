#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
CONTAINER_NAME="backup-container-$(date +%s)"
IMAGE_NAME="michadockermisha/backup:ubuntudesktop"
DUMP_DIR="/var/lib/vz/dump"

# List of files to copy
FILES=(
    "vzdump-lxc-101-2024_05_18-06_43_55.log"
    "vzdump-lxc-101-2024_05_18-06_48_28.log"
    "vzdump-lxc-101-2024_05_18-06_48_28.tmp"
    "vzdump-lxc-101-2024_06_05-23_04_40.log"
    "vzdump-lxc-101-2024_06_06-00_46_08.log"
    "vzdump-lxc-101-2024_06_06-01_22_03.log"
    "vzdump-lxc-101-2024_06_06-02_28_39.log"
    "vzdump-lxc-101-2024_06_06-15_02_50.log"
    "vzdump-lxc-101-2024_06_06-18_13_41.tmp"
    "vzdump-lxc-101-2024_06_06-19_34_36.log"
    "vzdump-lxc-101-2024_06_06-19_41_57.log"
    "vzdump-lxc-101-2024_06_07-12_45_40.log"
    "vzdump-lxc-101-2024_06_07-14_18_41.log"
    "vzdump-qemu-101-2024_08_31-15_25_54.log"
    "vzdump-qemu-101-2024_11_15-21_28_43.log"
    "vzdump-qemu-101-2024_11_15-21_29_11.log"
    "vzdump-qemu-101-2024_11_15-21_30_46.log"
    "vzdump-qemu-101-2024_11_21-22_17_51.log"
    "vzdump-qemu-101-2024_11_25-16_11_49.log"
    "vzdump-qemu-101-2024_11_25-16_11_49.vma.zst"
    "vzdump-qemu-101-2024_11_25-16_11_49.vma.zst.notes"
    "vzdump-qemu-102-2024_05_18-06_44_08.log"
    "vzdump-qemu-102-2024_05_18-06_54_28.log"
)

# Function to clean up the container in case of an error or exit
cleanup() {
    echo "Cleaning up..."
    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "Creating Alpine container named '$CONTAINER_NAME'..."
# Step 1: Create the Alpine container without starting it
docker create --name "$CONTAINER_NAME" alpine:latest

echo "Copying files to the container..."
# Step 2: Copy each specified file to /home in the container
for file in "${FILES[@]}"; do
    SRC_FILE="$DUMP_DIR/$file"
    if [[ -f "$SRC_FILE" ]]; then
        echo "Copying '$file' to /home/ in the container..."
        docker cp "$SRC_FILE" "$CONTAINER_NAME:/home/"
    else
        echo "Warning: File '$SRC_FILE' does not exist. Skipping."
    fi
done

echo "Committing the container to create a new image '$IMAGE_NAME'..."
# Step 3: Commit the container to create a new image
docker commit "$CONTAINER_NAME" "$IMAGE_NAME"

echo "Pushing the image to Docker repository..."
# Step 4: Push the image to the specified Docker repository
docker push "$IMAGE_NAME"

echo "Backup image '$IMAGE_NAME' created and pushed successfully."

# Cleanup is handled by the trap
