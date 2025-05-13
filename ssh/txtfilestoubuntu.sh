#!/bin/ 

# Define the source directory (current directory)
SOURCE_DIR=$(pwd)

# Define the destination directory on the remote machine
DESTINATION_DIR="ubuntu@192.168.1.193:/home/ubuntu/txt"

# Copy all .txt files from the source directory to the destination directory
scp "${SOURCE_DIR}"/*.txt "${DESTINATION_DIR}"
